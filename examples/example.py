from pdfimposer import TwoSidedFlip, bookletize_on_file

bookletize_on_file(
    input_file="./examples/a6_booklet.pdf",
    output_file="./examples/a6_booklet-imposed.pdf",
    layout="2x2",  # 8 A6 pages per A4 sheet
    page_format="A4",
    flip=TwoSidedFlip.LONG_EDGE,  # typical for booklet printing
    copy_pages=False,
)
