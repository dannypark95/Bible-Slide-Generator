from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def initialize_presentation():
    """
    Initializes a PowerPoint presentation object.
    """
    prs = Presentation()
    return prs

def add_textbox(slide, text, left, top, width, height, position, font_size):
    """
    Adds a text box to a slide.
    """
    textbox = slide.shapes.add_textbox(left, top, width, height)
    tf = textbox.text_frame
    tf.text = text
    p = tf.paragraphs[0]
    p.alignment = position

    for run in p.runs:
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(font_size)

def add_verse_slide(prs, verse_reference, verse_text):
    """
    Adds a single verse as a slide to the presentation.
    """
    slide_layout = prs.slide_layouts[6]  # Using a blank slide layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set slide background color to black
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 0, 0)
    
    # Verse reference in the top right
    add_textbox(slide, verse_reference, Inches(8.5), Inches(0), Inches(1.5), Inches(0.75), PP_ALIGN.RIGHT, 18)
    
    # Verse text
    add_textbox(slide, verse_text, Inches(0.5), Inches(2), Inches(9), Inches(5.5), PP_ALIGN.LEFT, 24)

def generate_presentation_for_chapter(book, chapter, verses):
    """
    Generates a presentation for a given book and chapter with each verse on a separate slide.
    """
    prs = initialize_presentation()
    for verse_number, verse_text in verses.items():
        verse_reference = f"{book} {chapter}:{verse_number}"
        add_verse_slide(prs, verse_reference, verse_text)
    
    file_name = f"{book}_{chapter}.pptx"
    save_presentation(prs, file_name)
    print(f"Presentation saved as {file_name}")

def save_presentation(prs, file_name):
    """
    Saves the presentation to a file.
    """
    prs.save(file_name)