class PdfConvError(Exception):
    """The base class for all exceptions raised by PdfImposer.

    The attribute "message" contains a message explaining the cause of the
    error.
    """

    def __init__(self, message: str | None = None) -> None:
        Exception.__init__(self)
        self.message = message


class MismatchingOrientationsError(PdfConvError):
    """This exception is raised if the required layout is incompatible with
    the input page orientation.

    The attribute "message" contains the problematic layout.
    """

    def __str__(self) -> str:
        return (
            f"The layout {self.message} is incompatible with the input page orientation"
        )


class UnknownFormatError(PdfConvError):
    """This exception is raised when the user tries to set an unknown page
    page_format.

    The attribute "message" contains the problematic page_format.
    """

    def __str__(self) -> str:
        return 'The page page_format "{self.message}" is unknown'


class UserInterruptError(PdfConvError):
    """This exception is raised when the user interrupts the conversion."""

    def __str__(self) -> str:
        return "User interruption"
