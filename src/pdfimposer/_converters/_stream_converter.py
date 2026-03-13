import pypdf

from pdfimposer._constants import PageOrientation, TwoSidedFlip
from pdfimposer._converters._abstract_converter import AbstractConverter
from pdfimposer._errors import MismatchingOrientationsError


class StreamConverter(AbstractConverter):
    """This class performs conversions on file-like objects (e.g. a StreamIO)."""

    def __init__(
        self,
        input_stream,
        output_stream,
        layout="2x1",
        page_format="A4",
        flip=TwoSidedFlip.SHORT_EDGE,
        copy_pages=False,
    ):
        """Create a StreamConverter.

        Args:
            input_stream: The file-like object from which tne input PDF:
                document should be read.
            output_stream: The file-like object to which tne output PDF:
                document should be written.
            layout: The layout of input pages on one output page (see:
                set_layout).
            page_format: The page_format of the output paper (see set_output_format).
            flip: Whether the output paper will be flipped on the short edge:
                (default) or the long edge when printing (see
                set_two_sided_flip).
            copy_pages: Whether the same group of input pages should be copied:
                to fill the corresponding output page or not (see
                set_copy_pages).
        """
        super().__init__(layout, page_format, flip, copy_pages)
        self._output_stream = output_stream
        self._input_stream = input_stream

        self._inpdf = pypdf.PdfReader(input_stream)

    def get_input_height(self):
        page = self._inpdf.pages[0]
        return int(page.mediabox.height)

    def get_input_width(self):
        page = self._inpdf.pages[0]
        return int(page.mediabox.width)

    def get_page_count(self):
        return len(self._inpdf.pages)

    def __fix_page_orientation(self, cmp):
        """Adapt the output page orientation.

        Args:
            cmp: A comparator function. Takes (number of pages on one):
                direction (int), number of pages on the other direction
                (int). Must return: the boolean result of the
                comparison.

        Raises:
            MismatchingOrientationsError: if the required layout is
                incompatible with the input page orientation.
        """
        if cmp(self.get_pages_in_width(), self.get_pages_in_height()):
            if self.get_input_orientation() == PageOrientation.PORTRAIT:
                if self._get_output_orientation() == PageOrientation.PORTRAIT:
                    self._set_output_orientation(PageOrientation.LANDSCAPE)
            else:
                raise MismatchingOrientationsError(self.get_layout())
        elif cmp(self.get_pages_in_height(), self.get_pages_in_width()):
            if self.get_input_orientation() == PageOrientation.LANDSCAPE:
                if self._get_output_orientation() == PageOrientation.LANDSCAPE:
                    self._set_output_orientation(PageOrientation.PORTRAIT)
            else:
                raise MismatchingOrientationsError(self.get_layout())
        else:
            if self.get_input_orientation() == PageOrientation.LANDSCAPE:
                if self._get_output_orientation() == PageOrientation.PORTRAIT:
                    self._set_output_orientation(PageOrientation.LANDSCAPE)
            else:
                if self._get_output_orientation() == PageOrientation.LANDSCAPE:
                    self._set_output_orientation(PageOrientation.PORTRAIT)

    def __fix_page_orientation_for_booklet(self):
        """Adapt the output page orientation to impose."""

        def __is_two_times(op1, op2):
            if op1 == 2 * op2:
                return True
            else:
                return False

        self.__fix_page_orientation(__is_two_times)

    def __fix_page_orientation_for_linearize(self):
        """Adapt the output page orientation to linearize."""

        def __is_half(op1, op2):
            if op2 == 2 * op1:
                return True
            else:
                return False

        self.__fix_page_orientation(__is_half)

    def __get_sequence_for_booklet(self):
        """Calculates the page sequence to impose a booklet.

        Returns:
            A list of page numbers representing sequence of pages to
            impose a booklet. The list might contain None where blank
            pages should be added.
        """
        n_pages = self.get_page_count()
        pages = list(range(0, n_pages))

        # Check for missing pages
        if (n_pages % 4) == 0:
            n_missing_pages = 0
        else:
            n_missing_pages = 4 - (n_pages % 4)
            # XXX: print a warning if input page number not divisible by 4?

        # Add reference to the missing empty pages to the pages sequence
        for missing_page in range(0, n_missing_pages):
            pages.append(None)

        def append_and_copy(list, pages):
            """Append pages to the list and copy them if needed."""
            if self.get_copy_pages():
                for i in range(int(self.get_pages_in_sheet() / 2)):
                    list.extend(pages)
            else:
                list.extend(pages)

        # Arranges the pages in booklet order
        sequence = []
        while pages:
            append_and_copy(sequence, [pages.pop(), pages.pop(0)])
            append_and_copy(sequence, [pages.pop(0), pages.pop()])

        return sequence

    def __get_sequence_for_linearize(self, booklet=True):
        """Calculates the page sequence to linearize a booklet.

        Returns:
            A list of page numbers representing sequence of pages to be
            extracted to linearize a booklet.
        """

        def append_and_remove_copies(list, pages):
            sequence.extend(pages)
            if self.get_copy_pages():
                for copy in range(self.get_pages_in_sheet() - len(pages)):
                    sequence.append(None)

        if booklet:
            sequence = []
            try:
                for i in range(0, self.get_page_count() * self.get_pages_in_sheet(), 4):
                    append_and_remove_copies(sequence, [int(i / 2), int(i / 2)])
                    append_and_remove_copies(sequence, [int(i / 2 + 1), int(i / 2 + 2)])
            except IndexError:
                # XXX: Print a warning
                pass
        else:
            sequence = list(range(0, self.get_page_count() * self.get_pages_in_sheet()))
        return sequence

    def __get_sequence_for_reduce(self):
        """Calculates the page sequence to linearly impose reduced pages.

        Returns:
            A list of page numbers representing sequence of pages to
            impose reduced pages. The list might contain None where
            blank pages should be added.
        """
        if self.get_copy_pages():
            sequence = []
            for page in range(self.get_page_count()):
                for copy in range(self.get_pages_in_sheet()):
                    sequence.append(page)
        else:
            sequence = list(range(self.get_page_count()))
            if len(sequence) % self.get_pages_in_sheet() != 0:
                for missing_page in range(
                    self.get_pages_in_sheet()
                    - (len(sequence) % self.get_pages_in_sheet())
                ):
                    sequence.append(None)
        return sequence

    def __write_output_stream(self, outpdf):
        """Writes output to the stream.

        Args:
            outpdf: the object to write to the stream. This object must have a:
                write() method.
        """
        self.get_progress_callback()("writing converted file", 1)
        outpdf.write(self._output_stream)
        self.get_progress_callback()("done", 1)

    def __do_reduce(self, sequence):
        """Do actual imposition job.

        Args:
            sequence: a list of page numbers representing the sequence of:
                pages to impose. None means blank page.
        """
        self.__fix_page_orientation_for_booklet()
        outpdf = pypdf.PdfWriter()

        current_page = 0
        output_page = 0
        while current_page < len(sequence):
            self.get_progress_callback()(
                (
                    "creating page "
                    f"{current_page + self.get_pages_in_sheet() / self.get_pages_in_sheet()}"  # noqa: E501
                ),
                float(current_page) / len(sequence),
            )
            page = outpdf.add_blank_page(
                self.get_output_width(), self.get_output_height()
            )
            for vert_pos in range(0, self.get_pages_in_height()):
                for horiz_pos in range(0, self.get_pages_in_width()):
                    if (
                        current_page < len(sequence)
                        and sequence[current_page] is not None
                    ):
                        source_page = self._inpdf.pages[sequence[current_page]]
                        tx = (
                            horiz_pos
                            * self.get_output_width()
                            / self.get_pages_in_width()
                        )
                        ty = self.get_output_height() - (
                            (vert_pos + 1)
                            * self.get_output_height()
                            / self.get_pages_in_height()
                        )
                        scale = self.get_reduction_factor()
                        op = (
                            pypdf.Transformation()
                            .scale(sx=scale, sy=scale)
                            .translate(tx=tx, ty=ty)
                        )
                        page.merge_transformed_page(source_page, op)
                        current_page += 1
            if self.get_two_sided_flip() == TwoSidedFlip.LONG_EDGE and output_page % 2:
                page.rotate(180)
            page.compress_content_streams()
            output_page += 1
        self.__write_output_stream(outpdf)

    def bookletize(self):
        self.__do_reduce(self.__get_sequence_for_booklet())

    def reduce(self):
        self.__do_reduce(self.__get_sequence_for_reduce())

    def linearize(self, booklet=True):
        self.__fix_page_orientation_for_linearize()
        sequence = self.__get_sequence_for_linearize()
        outpdf = pypdf.PdfWriter()

        output_page = 0
        for input_page in range(0, self.get_page_count()):
            for vert_pos in range(0, self.get_pages_in_height()):
                for horiz_pos in range(0, self.get_pages_in_width()):
                    if sequence[output_page] is not None:
                        self.get_progress_callback()(
                            f"extracting page {output_page + 1}",
                            float(output_page) / len(sequence),
                        )
                        page = outpdf.insert_blank_page(
                            self.get_output_width(),
                            self.get_output_height(),
                            sequence[output_page],
                        )
                        page.mergeScaledTranslatedPage(
                            self._inpdf.pages[input_page],
                            self.get_increasing_factor(),
                            -horiz_pos * self.get_output_width(),
                            (vert_pos - self.get_pages_in_height() + 1)
                            * self.get_output_height(),
                        )
                        page.compress_content_streams()
                    output_page += 1
        self.__write_output_stream(outpdf)
