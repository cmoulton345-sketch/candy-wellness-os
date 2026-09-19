import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

pdf_path = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC/Rayne_AP_Anatomical_Blueprints_Master.pdf"
img_dir = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC/images"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Custom Styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=colors.HexColor('#880e4f'),
    alignment=TA_CENTER
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#4a148c'),
    alignment=TA_CENTER
)

heading_style = ParagraphStyle(
    'SectionHeading',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#880e4f'),
    spaceAfter=6
)

body_bold = ParagraphStyle(
    'BodyBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#0f172a')
)

body_text = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#334155')
)

story = []

# --- COVER HEADER ---
story.append(Paragraph("ANATOMY & PHYSIOLOGY MASTER BLUEPRINTS", title_style))
story.append(Spacer(1, 4))
story.append(Paragraph("NBCC Practical Nursing (HCSS1087A) • Instructor: Jessica Freeze Snyder • Student: Rayne Moulton", subtitle_style))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#880e4f'), spaceAfter=15))

# ================= PAGE 1: THE HUMAN CELL =================
story.append(Paragraph("BLUEPRINT 1: THE HUMAN CELL STRUCTURE & FUNCTION", heading_style))

cell_img = os.path.join(img_dir, "cell_diagram.png")
if os.path.exists(cell_img):
    story.append(Image(cell_img, width=480, height=280))
    story.append(Spacer(1, 10))

# Cell Table
cell_data = [
    [Paragraph("Organelle / Part", body_bold), Paragraph("Structure Description", body_bold), Paragraph("Primary Physiological Function", body_bold)],
    [Paragraph("Plasma Membrane", body_bold), Paragraph("Semipermeable lipid bilayer enclosing cytoplasm.", body_text), Paragraph("Protects cell integrity; regulates entry/exit of nutrients & waste.", body_text)],
    [Paragraph("Nucleus", body_bold), Paragraph("Control center housing 46 chromosomes (DNA).", body_text), Paragraph("Directs all cellular functions, growth, and division (mitosis).", body_text)],
    [Paragraph("Cytoplasm", body_bold), Paragraph("Internal gel-like fluid medium (cytosol).", body_text), Paragraph("Houses and suspends all cell organelles, ions, and metabolic enzymes.", body_text)],
    [Paragraph("Ribosomes", body_bold), Paragraph("Tiny granules free in cytoplasm or on Rough ER.", body_text), Paragraph("'Protein factories' that synthesize vital structural & enzymatic proteins.", body_text)],
    [Paragraph("Mitochondria", body_bold), Paragraph("Double-membrane oval organelle.", body_text), Paragraph("'Powerhouse' that extracts food energy & converts it into ATP fuel.", body_text)]
]

t_cell = Table(cell_data, colWidths=[110, 180, 250])
t_cell.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fce4ec')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#880e4f')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#f8bbd0')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_cell)
story.append(PageBreak())

# ================= PAGE 2: INTEGUMENTARY SYSTEM =================
story.append(Paragraph("BLUEPRINT 2: THE INTEGUMENTARY SYSTEM (SKIN, GLANDS, RECEPTORS)", heading_style))

skin_img = os.path.join(img_dir, "skin_diagram.png")
if os.path.exists(skin_img):
    story.append(Image(skin_img, width=500, height=280))
    story.append(Spacer(1, 10))

# Receptors Table
rec_data = [
    [Paragraph("Cutaneous Receptor", body_bold), Paragraph("Location in Skin", body_bold), Paragraph("Sensation Detected", body_bold)],
    [Paragraph("Meissner's Corpuscle", body_bold), Paragraph("Dermal Papillae (Papillary Dermis)", body_text), Paragraph("Light touch, texture, and light vibration", body_text)],
    [Paragraph("Pacinian Corpuscle", body_bold), Paragraph("Reticular Dermis / Hypodermis", body_text), Paragraph("Deep pressure and fast vibration", body_text)],
    [Paragraph("Ruffini's End Organ", body_bold), Paragraph("Dermis", body_text), Paragraph("Skin stretch detection", body_text)],
    [Paragraph("End Bulb of Krause", body_bold), Paragraph("Dermis", body_text), Paragraph("Cold temperature detection", body_text)],
    [Paragraph("Merkel's Disc", body_bold), Paragraph("Epidermis / Dermis Junction", body_text), Paragraph("Sustained touch and pressure", body_text)],
    [Paragraph("Free Nerve Endings", body_bold), Paragraph("Epidermis & Dermis", body_text), Paragraph("Pain and itching sensations", body_text)]
]

t_rec = Table(rec_data, colWidths=[130, 180, 230])
t_rec.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0f2fe')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0369a1')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bae6fd')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t_rec)
story.append(PageBreak())

# ================= PAGE 3: SKELETAL SYSTEM =================
story.append(Paragraph("BLUEPRINT 3: THE SKELETAL SYSTEM & JOINTS", heading_style))

skel_img = os.path.join(img_dir, "skel_diagram.png")
if os.path.exists(skel_img):
    story.append(Image(skel_img, width=500, height=240))
    story.append(Spacer(1, 10))

# Skeletal Breakdown Table
skel_data = [
    [Paragraph("Skeleton Division", body_bold), Paragraph("Bone Count", body_bold), Paragraph("Major Bones Included", body_bold)],
    [Paragraph("Axial Skeleton", body_bold), Paragraph("80 Bones", body_bold), Paragraph("Skull (8 cranial, 14 facial), Hyoid bone, Vertebral Column (26 vertebrae), Thorax (Sternum & 12 pairs of ribs).", body_text)],
    [Paragraph("Appendicular Skeleton", body_bold), Paragraph("126 Bones", body_bold), Paragraph("Pectoral Girdle (Scapula, Clavicle), Upper Limbs (Humerus, Radius, Ulna, Carpals, Metacarpals, Phalanges), Pelvic Girdle, Lower Limbs (Femur, Patella, Tibia, Fibula, Tarsals, Metatarsals, Phalanges).", body_text)]
]

t_skel = Table(skel_data, colWidths=[120, 80, 340])
t_skel.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fef08a')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#713f12')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#fde047')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_skel)
story.append(Spacer(1, 10))

# Cartilage & Joints Table
cj_data = [
    [Paragraph("Category", body_bold), Paragraph("Types / Classifications", body_bold), Paragraph("Anatomical Locations & Mobility", body_bold)],
    [Paragraph("Cartilage Types", body_bold), Paragraph("1. Hyaline (Articular)<br/>2. Elastic<br/>3. Fibrocartilage", body_text), Paragraph("• Hyaline: Covers bone ends at joints & rib connections.<br/>• Elastic: Springy cartilage in ear & epiglottis.<br/>• Fibrocartilage: Tough shock absorber in intervertebral discs & pubic symphysis.", body_text)],
    [Paragraph("Joint Mobility", body_bold), Paragraph("1. Synarthrosis<br/>2. Amphiarthrosis<br/>3. Diarthrosis", body_text), Paragraph("• Synarthrosis: Immovable joints (e.g. skull sutures).<br/>• Amphiarthrosis: Slightly movable (e.g. pubic symphysis).<br/>• Diarthrosis: Freely movable synovial joints (e.g. shoulder, knee).", body_text)]
]

t_cj = Table(cj_data, colWidths=[100, 140, 300])
t_cj.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ccfbf1')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f766e')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_cj)

doc.build(story)
print("Saved Master PDF to:", pdf_path)
