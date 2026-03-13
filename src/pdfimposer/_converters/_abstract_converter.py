import types
from abc import ABCMeta, abstractmethod

from pdfimposer._constants import PAGE_FORMATS, PageOrientation, TwoSidedFlip
from pdfimposer._errors import UnknownFormatError


class AbstractConverter(metaclass=ABCMeta):
    """The base class for all pdfimposer converter classes.

    It is an abstract class, with some abstract functions which should be
    overridden :
    - get_input_height
    - get_input_width
    - get_page_count
    - bookletize
    - linearize
    - reduce
    """

    page_formats = PAGE_FORMATS

    def __init__(
        self,
        layout="2x1",
        page_format="A4",
        flip=TwoSidedFlip.SHORT_EDGE,
        copy_pages=False,
    ):
        """Create an AbstractConverter instance.

        Args:
            layout: The layout of input pages on one output page:
                (see set_layout).
            page_format: The page_format of the output paper (see:
                set_output_format).
            flip: Render the output booklet for two-sided printing with:
                flipping on the short (default) or long edge. Long-edge
                flip will result in even-numbered output pages being
                upside-down.
            copy_pages: Whether the same group of input pages: should
                be copied to fill the corresponding output page or not
                (see set_copy_pages).
        """
        self.layout = None
        self.output_format = None
        self.output_orientation = None

        self.set_layout(layout)
        self.set_output_format(page_format)
        self.set_copy_pages(copy_pages)
        self.set_two_sided_flip(flip)

        def default_progress_callback(msg, prog):
            print(f"{msg} ({prog * 100}%)")

        self.set_progress_callback(default_progress_callback)

    def set_output_height(self, height):
        """Set the height of the output page.

        Args:
            height: The height of the output page in default user space units.
        """
        self.__output_height = int(height)

    def get_output_height(self):
        """Get the height of the output page.

        Returns:
            The height of the output page in default user space units.
        """
        return self.__output_height

    def set_output_width(self, width):
        """Set the width of the output page.

        Args:
            width: The height of the output page in default user space units.
        """
        self.__output_width = int(width)

    def get_output_width(self):
        """Get the width of the output page.

        Returns:
            The width of the output page in default user space units.
        """
        return self.__output_width

    def set_pages_in_width(self, num):
        """Set the number of input pages to put in the width on one output page.

        Args:
            num: An integer representing the number of pages in width.
        """
        self.__pages_in_width = int(num)

    def get_pages_in_width(self):
        """Get the number of input pages to put in the width on one output page.

        Returns:
            An integer representing the number of pages in width.
        """
        return self.__pages_in_width

    def set_pages_in_height(self, num):
        """Set the number of input pages to put in the height on one output page.

        Args:
            num: An integer representing the number of pages in height.
        """
        self.__pages_in_height = int(num)

    def get_pages_in_height(self):
        """Get the number of input pages to put in the height on one output page.

        Returns:
            An integer representing the number of pages in height.
        """
        return self.__pages_in_height

    def set_copy_pages(self, copy_pages):
        """Set whether the same group of input pages should be copied to fill the
        corresponding output page or not.

        Args:
            copy_pages: True to get copies of the same group of input page:
                on one output page. False to get different groups of
                input pages on one output page.
        """
        self.__copy_pages = bool(copy_pages)

    def get_copy_pages(self):
        """Get whether the same group of input pages will be copied to fill the
        corresponding output page or not.

        Returns:
            True if copies of the same group of input page will get
            copied on one output page. False if different groups of input
            pages will go on one output page.
        """
        return self.__copy_pages

    def set_progress_callback(self, progress_callback):
        """Register a progress callback function.

        Register a callback function that will be called to inform on the
        progress of the conversion.

        Args:
            progress_callback: The callback function which is called to:
                return the conversion progress. Its signature must be :
                a string for the progress message; a number in the range
                [0, 1] for the progress.
        """
        assert isinstance(progress_callback, types.FunctionType)
        self.__progress_callback = progress_callback

    def get_progress_callback(self):
        """Get the progress callback function.

        Get the callback function that will be called to inform on the
        progress of the conversion.

        Returns:
            The callback function which is called to return the conversion progress.
        """
        return self.__progress_callback

    def set_two_sided_flip(self, flip):
        """Set the edge which the paper will be flipped on when printed. Defaults
        to TwoSidedFlip.SHORT_EDGE, where all the output pages are the right
        way up. If your printer can only flip over the long edge, set this to
        TwoSidedFlip.LONG_EDGE. The imposer will rotate all even output pages
        180° to compensate.

        Args:
            flip: Either TwoSidedFlip.SHORT_EDGE or TwoSidedFlip.LONG_EDGE.
        """
        assert flip in (TwoSidedFlip.SHORT_EDGE, TwoSidedFlip.LONG_EDGE)
        self.__two_sided_flip = flip

    def get_two_sided_flip(self):
        """Get the edge which the paper will be flipped on when printed.

        Returns:
            Either TwoSidedFlip.SHORT_EDGE or TwoSidedFlip.LONG_EDGE.
        """
        return self.__two_sided_flip

    # SOME GETTERS THAT CALCULATE THE VALUE THEY RETURN FROM OTHER VALUES
    def get_input_size(self):
        """Return the page size of the input document.

        Returns:
            A tuple (width, height) representing the page size of the
            input document expressed in default user space units.
        """
        return (self.get_input_width(), self.get_input_height())

    @abstractmethod
    def get_input_height(self):
        """Return the page height of the input document.

        Returns:
            The page height of the input document expressed in default
            user space units.
        """
        ...

    @abstractmethod
    def get_input_width(self):
        """Return the page width of the input document.

        Returns:
            The page width of the input document expressed in default
            user space units.
        """
        ...

    def get_input_orientation(self):
        """Return the page orientation of the input document.

        Returns:
            A constant from PageOrientation, or None (if square paper).
        """
        if self.get_input_height() > self.get_input_width():
            return PageOrientation.PORTRAIT
        elif self.get_input_height() < self.get_input_width():
            return PageOrientation.LANDSCAPE
        else:
            # XXX: is square
            return None

    def set_layout(self, layout):
        """Set the layout of input pages on one output page.

        Args:
            layout: A string of the form WxH, or a tuple or list of the form:
                (W, H), where W is the number of input pages to put on
                the width of the output page and H is the number of
                input pages to put in the height of an output page.
        """
        if isinstance(layout, str):
            pages_in_width, pages_in_height = layout.split("x")
        elif isinstance(layout, list | tuple) and (len(layout) == 2):
            pages_in_width, pages_in_height = layout
        else:
            raise ValueError
        self.set_pages_in_width(int(pages_in_width))
        self.set_pages_in_height(int(pages_in_height))

    def get_layout(self):
        """Return the layout of input pages on one output page.

        Returns:
            A string of the form WxH, where W is the number of input
            pages to put on the width of the output page and H is the
            number of input pages to put in the height of an output
            page.
        """
        return str(self.get_pages_in_width()) + "x" + str(self.get_pages_in_height())

    def get_pages_in_sheet(self):
        """Calculate the number of input page that will be put on one output page.

        Returns:
            An integer representing the number of input pages on one
            output page.
        """
        return self.get_pages_in_width() * self.get_pages_in_height()

    def set_output_format(self, page_format):
        """Set the page_format of the output paper.

        Args:
            page_format: A string representing name of the the desired paper:
                page_format, among the keys of page_formats (e.g. A3, A4,
                A5).

        Raises:
            UnknownFormatError: if the given paper page_format is not recognized.
        """
        if page_format in self.page_formats:
            width, height = self.page_formats[page_format]
            self.set_output_height(height)
            self.set_output_width(width)
        else:
            raise UnknownFormatError(page_format)

    def get_output_format(self):
        """Return the page_format of the output paper.

        Returns:
            A string representing the name of the paper page_format (e.g. A3, A4, A5).
        """
        return next(
            page_format
            for page_format, dimensions in self.page_formats.items()
            if dimensions == (self.get_output_width, self.get_output_height)
        )

    def get_input_format(self):
        """Return the page_format of the input paper.

        Returns:
            A string representing the name of the paper page_format (e.g. A3, A4, A5).
        """
        width, height = self.get_input_size()
        if self.get_input_orientation() == PageOrientation.LANDSCAPE:
            size = height, width
        else:
            size = width, height
        return next(
            page_format
            for page_format, dimensions in self.page_formats.items()
            if dimensions == size
        )

    @abstractmethod
    def get_page_count(self):
        """Return the number of pages of the input document.

        Returns:
            The number of pages of the input document.
        """
        ...

    def get_reduction_factor(self):
        """Calculate the reduction factor.

        Returns:
            The reduction factor to be applied to an input page to obtain its size on
                the output page.
        """
        return float(self.get_output_width()) / (
            self.get_pages_in_width() * self.get_input_width()
        )

    def get_increasing_factor(self):
        """Calculate the increasing factor.

        Returns:
            The increasing factor to be applied to an input page to obtain its size
                on the output page.
        """
        return (
            float(self.get_pages_in_width() * self.get_output_width())
            / self.get_input_width()
        )

    def _set_output_orientation(self, output_orientation):
        """Set the orientation of the output paper.

        WARNING: in the current implementation, the orientation of the output paper may
        be automatically adjusted, even if it was set manually.

        Args:
            output_orientation: A constant from PageOrientation, or
                None (if square paper).
        """
        output_orientation = bool(output_orientation)

        w = self.get_output_width()
        h = self.get_output_height()

        if (output_orientation == PageOrientation.PORTRAIT and w > h) or (
            output_orientation == PageOrientation.LANDSCAPE and h > w
        ):
            self.set_output_height(w)
            self.set_output_width(h)

    def _get_output_orientation(self):
        """Return the orientation of the output paper.

        WARNING: in the current implementation, the orientation of the
        output paper may be automatically adjusted, even if it was set
        manually.

        Returns:
            A constant among from PageOrientation, or None (if square
            paper).
        """
        if self.get_output_height() > self.get_output_width():
            return PageOrientation.PORTRAIT
        elif self.get_output_height() < self.get_output_width():
            return PageOrientation.LANDSCAPE
        else:
            return None

    # CONVERSION FUNCTIONS
    @abstractmethod
    def bookletize(self):
        """Convert a linear document to a booklet.

        Convert a linear document to a booklet, arranging the pages as
        required.
        """
        ...

    @abstractmethod
    def linearize(self):
        """Convert a booklet to a linear document.

        Convert a booklet to a linear document, arranging the pages as
        required.
        """
        ...

    @abstractmethod
    def reduce(self):
        """Put multiple input pages on one output page."""
        ...
