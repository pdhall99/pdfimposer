import os
import re
import types

from pdfimposer._constants import TwoSidedFlip
from pdfimposer._converters._stream_converter import StreamConverter
from pdfimposer._errors import UserInterruptError


class FileConverter(StreamConverter):
    """This class performs conversions on true files."""

    def __init__(
        self,
        infile_name,
        outfile_name=None,
        layout="2x1",
        page_format="A4",
        flip=TwoSidedFlip.SHORT_EDGE,
        copy_pages=False,
        overwrite_outfile_callback=None,
    ):
        """Create a FileConverter.

        Args:
            infile_name: The name of the input PDF file.
            outfile_name: The name of the file where the output PDF:
                should be written. If omitted, defaults to the name of
                the input PDF postponded by '-conv'.
            layout: The layout of input pages on one output page (see:
                set_layout).
            page_format: The page_format of the output paper (see set_output_format).
            copy_pages: Whether the same group of input pages should be copied:
                to fill the corresponding output page or not (see
                set_copy_pages).
            flip: Whether the output paper will be flipped on the short edge:
                (default) or the long edge when printing (see
                set_two_sided_flip).
            overwrite_outfile_callback: A callback function which is called:
                if outfile_name already exists when trying to open it.
                Its signature must be : take a string for the
                outfile_name as an argument;

                return False not to overwrite the file. If omitted, existing file
                would be overwritten without confirmation.
        """
        # sets [input, output]_stream to None so we can test their presence
        # in __del__
        self._input_stream = None
        self._output_stream = None

        # outfile_name is set if provided
        if outfile_name:
            self.__set_outfile_name(outfile_name)
        else:
            self.__set_outfile_name(None)

        # Then infile_nameis set, so if outfile_name was not provided we
        # can create it from infile_name
        self.__set_infile_name(infile_name)

        # Setup callback to ask for confirmation before overwriting outfile
        if overwrite_outfile_callback:
            assert isinstance(overwrite_outfile_callback, types.FunctionType)
        else:

            def overwrite_outfile_callback(filename):
                return True

        # Now initialize a streamConverter
        self._input_stream = open(self.get_infile_name(), "rb")
        outfile_name = self.get_outfile_name()
        if os.path.exists(outfile_name) and not overwrite_outfile_callback(
            os.path.abspath(outfile_name)
        ):
            raise UserInterruptError()
        self._output_stream = open(outfile_name, "wb")
        StreamConverter.__init__(
            self,
            self._input_stream,
            self._output_stream,
            layout,
            page_format,
            flip,
            copy_pages,
        )

    def __del__(self):
        if self._input_stream:
            try:
                self._input_stream.close()
            except OSError:
                # XXX: Do something better
                pass
        if self._output_stream:
            try:
                self._output_stream.close()
            except OSError:
                # XXX: Do something better
                pass

    # GETTERS AND SETTERS SECTION
    def __set_infile_name(self, name):
        """Sets the name of the input PDF file. Also set the name of output PDF
        file if not already set.

        Args:
            name: the name of the input PDF file.
        """
        self.__infile_name = name

        if not self.__outfile_name:
            result = re.search(r"(.+)\.\w*$", name)
            if result:
                self.__outfile_name = result.group(1) + "-conv.pdf"
            else:
                self.__outfile_name = name + "-conv.pdf"

    def get_infile_name(self):
        """Get the name of the input PDF file.

        Returns:
            The name of the input PDF file.
        """
        return self.__infile_name

    def __set_outfile_name(self, name):
        """Sets the name of the output PDF file.

        Args:
            name: the name of the output PDF file.
        """
        self.__outfile_name = name

    def get_outfile_name(self):
        """Get the name of the output PDF file.

        Returns:
            The name of the output PDF file.
        """
        return self.__outfile_name
