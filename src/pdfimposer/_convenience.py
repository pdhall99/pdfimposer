from pdfimposer._constants import TwoSidedFlip
from pdfimposer._converters._file_converter import FileConverter
from pdfimposer._converters._stream_converter import StreamConverter


def bookletize_on_stream(
    input_stream,
    output_stream,
    layout="2x1",
    page_format="A4",
    flip=TwoSidedFlip.SHORT_EDGE,
    copy_pages=False,
):
    """Convert a linear document to a booklet.

    Convert a linear document to a booklet, arranging the pages as
    required.

    This is a convenience function around StreamConverter

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
    StreamConverter(
        layout, page_format, flip, copy_pages, input_stream, output_stream()
    ).bookletize()


def bookletize_on_file(
    input_file,
    output_file=None,
    layout="2x1",
    page_format="A4",
    flip=TwoSidedFlip.SHORT_EDGE,
    copy_pages=False,
):
    """Convert a linear PDF file to a booklet.

    Convert a linear PDF file to a booklet, arranging the pages as
    required.

    This is a convenience function around FileConverter

    Args:
        input_file: The name to the input PDF file.
        output_file: The name of the file where the output PDF:
            should be written. If omitted, defaults to the name of the
            input PDF postponded by '-conv'.
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
    FileConverter(
        input_file, output_file, layout, page_format, flip, copy_pages
    ).bookletize()


def linearize_on_stream(
    input_stream, output_stream, layout="2x1", page_format="A4", copy_pages=False
):
    """Convert a booklet to a linear document.

    Convert a booklet to a linear document, arranging the pages as
    required.

    This is a convenience function around StreamConverter

    Args:
        input_stream: The file-like object from which tne input PDF:
            document should be read.
        output_stream: The file-like object to which tne output PDF:
            document should be written.
        layout: The layout of output pages on one input page (see:
            set_layout).
        page_format: The page_format of the output paper (see set_output_format).
        copy_pages: Whether the same group of input pages should be copied:
            to fill the corresponding output page or not (see
            set_copy_pages).
    """
    StreamConverter(
        input_stream,
        output_stream,
        layout,
        page_format,
        TwoSidedFlip.SHORT_EDGE,
        copy_pages,
    ).linearize()


def linearize_on_file(
    input_file,
    output_file=None,
    layout="2x1",
    page_format="A4",
    flip=TwoSidedFlip.SHORT_EDGE,
    copy_pages=False,
):
    """Convert a booklet to a linear PDF file.

    Convert a booklet to a linear PDF file, arranging the pages as
    required.

    This is a convenience function around FileConverter

    Args:
        input_file: The name to the input PDF file.
        output_file: The name of the file where the output PDF:
            should be written. If omitted, defaults to the name of the
            input PDF postponded by '-conv'.
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
    FileConverter(
        input_file, output_file, layout, page_format, flip, copy_pages
    ).linearize()


def reduce_on_stream(
    input_stream,
    output_stream,
    layout="2x1",
    page_format="A4",
    flip=TwoSidedFlip.SHORT_EDGE,
    copy_pages=False,
):
    """Put multiple input pages on one output page.

    This is a convenience function around StreamConverter

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
    StreamConverter(
        input_stream, output_stream, layout, page_format, flip, copy_pages
    ).reduce()


def reduce_on_file(
    input_file,
    output_file=None,
    layout="2x1",
    page_format="A4",
    flip=TwoSidedFlip.SHORT_EDGE,
    copy_pages=False,
):
    """Put multiple input pages on one output page.

    This is a convenience function around FileConverter

    Args:
        input_file: The name to the input PDF file.
        output_file: The name of the file where the output PDF:
            should be written. If omitted, defaults to the name of the
            input PDF postponded by '-conv'.
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
    FileConverter(
        input_file, output_file, layout, page_format, flip, copy_pages
    ).reduce()
