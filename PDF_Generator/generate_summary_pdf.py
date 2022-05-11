import os
from pathlib import Path
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_summary_pdf(SUMMARY_PATH, emailhash, fileid, IMAGES_PATH = None):
    OUTPUT_PATH = os.path.join(os.path.join(Path(SUMMARY_PATH).parent.parent, emailhash), "SUMMARY")
    doc = SimpleDocTemplate(os.path.join(OUTPUT_PATH, f"{fileid}_SUMMARY.pdf"),pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    with open(SUMMARY_PATH) as f:
        txt_heading = "<b>Textual Summary</b>"
        Story.append(Paragraph(txt_heading, styles['Center']))
        Story.append(Spacer(1, 12))
        contents = f.read()
        paragraphs = contents.split("\n\n")
        for paragraph in paragraphs:
            Story.append(Paragraph(paragraph, styles["Justify"]))       
            Story.append(Spacer(1, 12))
    Story.append(PageBreak())
    if IMAGES_PATH:
        img_heading = "<b>Generated Key Frames</b>"
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(img_heading, styles['Center']))
        
        chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
        for i in range(0, len(os.listdir(IMAGES_PATH))-1, 2):
            if (len(os.listdir(IMAGES_PATH))-i-2) == 0:
                break
            Story.append(Table([[Image(os.path.join(IMAGES_PATH, f"{fileid}_{i}.jpeg"), 3.5 * inch, 2.5 * inch), Image(os.path.join(IMAGES_PATH, f"{fileid}_{i+1}.jpeg"), 3.5 * inch, 2.5 * inch)]],
                     colWidths=[4.5 * inch, 4.5 * inch],
                     rowHeights=[3.5 * inch], style=chart_style))
        if (len(os.listdir(IMAGES_PATH))-1)%2:
            Story.append(Table([[Image(os.path.join(IMAGES_PATH, f"{fileid}_{len(os.listdir(IMAGES_PATH))-2}.jpeg"), 3.5 * inch, 2.5 * inch)]],
                colWidths=[4.5 * inch, 4.5 * inch],
                rowHeights=[3.5 * inch], style=chart_style))
    print("Generated pdf\n\n\n")
    doc.build(Story)