"""Converts PDF documents between different page layouts.

This module enables to:
 - convert linear (page by page) PDF documents to booklets;
 - revert booklets to linear documents;
 - reduce multiple input PDF pages and put them on one single output page.

The `StreamConverter` class works on StreamIO, while the `FileConverter`
class works on files.

Some convenience functions are also provided.
"""

from pdfimposer._constants import PageOrientation, TwoSidedFlip
from pdfimposer._convenience import (
    bookletize_on_file,
    bookletize_on_stream,
    linearize_on_file,
    linearize_on_stream,
    reduce_on_file,
    reduce_on_stream,
)
from pdfimposer._converters._abstract_converter import AbstractConverter
from pdfimposer._converters._file_converter import FileConverter
from pdfimposer._converters._stream_converter import StreamConverter
from pdfimposer._errors import (
    MismatchingOrientationsError,
    PdfConvError,
    UnknownFormatError,
    UserInterruptError,
)

__all__ = [
    "bookletize_on_stream",
    "bookletize_on_file",
    "linearize_on_stream",
    "linearize_on_file",
    "reduce_on_stream",
    "reduce_on_file",
    "PageOrientation",
    "TwoSidedFlip",
    "UnknownFormatError",
    "MismatchingOrientationsError",
    "PdfConvError",
    "UnknownFormatError",
    "UserInterruptError",
    "AbstractConverter",
    "FileConverter",
    "StreamConverter",
]
