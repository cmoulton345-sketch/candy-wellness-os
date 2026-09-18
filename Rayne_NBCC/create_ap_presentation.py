import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_ap_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme colors for A&P (Deep Crimson / Magenta & Rose)
    CRIMSON = RGBColor(136, 14, 79)       # #880e4f
    ROSE_LIGHT = RGBColor(252, 228, 236)  # background light
    DARK_NAVY = RGBColor(33, 33, 33)
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(250, 245, 248)
    CARD_BORDER = RGBColor(220, 180, 200)
    ACCENT_MAGENTA = RGBColor(194, 24, 91)

    def add_header(slide, title_text, category_text="HCSS1087A • ANATOMY & PHYSIOLOGY"):
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.2))
        header.fill.solid()
        header.fill.fore_color.rgb = CRIMSON
        header.line.color.rgb = CRIMSON

        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(248, 187, 208)

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    # --- SLIDE 1: Title Slide ---
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = CRIMSON

    tbox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "HCSS1087A — Anatomy & Physiology"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(248, 187, 208)

    p2 = tf1.add_paragraph()
    p2.text = "Module 3: The Integumentary System"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Skin Layers • Accessory Organs • Cutaneous Receptors • 6 Functions"
    p3.font.size = Pt(22)
    p3.font.color.rgb = RGBColor(252, 228, 236)
    p3.space_before = Pt(15)

    p4 = tf1.add_paragraph()
    p4.text = "Instructor: Jessica Freeze Snyder | Practical Nursing Study Suite for Rayne Moulton"
    p4.font.size = Pt(16)
    p4.font.italic = True
    p4.font.color.rgb = RGBColor(244, 143, 177)
    p4.space_before = Pt(35)

    # --- SLIDE 2: Skin Layers ---
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Module 3: Primary Layers of Human Skin")

    layers = [
        ("Epidermis (Outermost)", [
            "Nonvascular (no blood vessels; nourished by dermis)",
            "5 distinct layers: Basale, Spinosum, Granulosum, Lucidum, Corneum",
            "95% Keratinocytes (tough waterproof keratin protein)",
            "5% Melanocytes (melanin pigment for skin color)"
        ]),
        ("Dermis (Middle Layer)", [
            "20x thicker than epidermis; mainly connective tissue",
            "Collagen fibers (tough/strong) & Elastic fibers (stretch)",
            "Papillary Layer: Dermal papillae (fingerprints) & touch receptors",
            "Reticular Layer: Blood vessels, glands, hair follicles, Pacinian corpuscles"
        ]),
        ("Hypodermis (Foundation)", [
            "Also called Subcutaneous Tissue or Superficial Fascia",
            "Composed mostly of Adipose (fat) tissue",
            "Stores fat for energy, provides thermal insulation & cushioning",
            "Attaches skin securely to underlying muscles & bones"
        ])
    ]

    for i, (title, bullets) in enumerate(layers):
        left = Inches(0.8 + i * 3.9)
        top = Inches(1.6)
        width = Inches(3.6)
        height = Inches(5.3)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        tb = slide2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(17)
        pt.font.bold = True
        pt.font.color.rgb = CRIMSON

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(13)
            pb.font.color.rgb = DARK_NAVY
            pb.space_before = Pt(8)

    # --- SLIDE 3: Accessory Organs ---
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Module 3: Accessory Organs (Hair, Nails, Glands)")

    organs = [
        ("Hair & Arrector Pili", "Hair Shaft (visible), Root (in follicle), Papilla/Bulb (base growth cluster nourished by blood vessels).\nArrector Pili muscle contracts for 'goosebumps' when cold/scared."),
        ("Nails & Cyanosis", "Nail Body (visible keratin plate), Root (hidden in groove), Lunula (white crescent area).\nCyanosis: bluish nail bed color from poor blood oxygenation."),
        ("Eccrine Sweat Glands", "Most abundant all over body. Secrete thin watery perspiration continuously for temperature cooling and waste elimination."),
        ("Apocrine Sweat Glands", "Axilla, groin, nipples. Secrete thicker fluid in spurts. Odorless until acted upon by skin microbes/bacteria."),
        ("Sebaceous (Oil) Glands", "Everywhere hair grows; secrete Sebum ('nature's skin cream') to prevent cracking. Trapped sebum forms whiteheads (pimples) or blackheads."),
        ("Cutaneous Absorption", "Skin absorbs lipid-soluble drugs via passive diffusion (e.g. transdermal nitroglycerin/hormone patches).")
    ]

    for idx, (o_name, o_desc) in enumerate(organs):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 3.9)
        top = Inches(1.6 + row * 2.7)
        width = Inches(3.6)
        height = Inches(2.4)

        b_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        b_box.fill.solid()
        b_box.fill.fore_color.rgb = CARD_BG
        b_box.line.color.rgb = CARD_BORDER

        tb = slide3.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = o_name
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = CRIMSON

        p2 = tf.add_paragraph()
        p2.text = o_desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = DARK_NAVY
        p2.space_before = Pt(6)

    # --- SLIDE 4: Mechanoreceptors ---
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Module 3: Cutaneous Mechanoreceptors (Sensation)")

    receptors = [
        ("Meissner's Corpuscle", "Texture & light vibration / touch (located in dermal papillae)."),
        ("Pacinian Corpuscle", "Deep pressure & fast vibration (located in reticular dermis/hypodermis)."),
        ("Ruffini's End Organ", "Skin stretch detection."),
        ("End Bulb of Krause", "Cold temperature detection."),
        ("Merkel's Disc", "Sustained touch and pressure."),
        ("Free Nerve Endings", "Pain and itching sensations (unencapsulated).")
    ]

    for idx, (r_name, r_desc) in enumerate(receptors):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.6 + row * 1.8)
        width = Inches(5.6)
        height = Inches(1.6)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        tb = slide4.shapes.add_textbox(left + Inches(0.15), top + Inches(0.1), width - Inches(0.3), height - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = r_name
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = ACCENT_MAGENTA

        p2 = tf.add_paragraph()
        p2.text = "Function / Sensation: " + r_desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK_NAVY
        p2.space_before = Pt(4)

    # --- SLIDE 5: 6 Functions & Exam Takeaways ---
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "6 Core Functions of the Skin & Exam Strategy")

    box_s = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    box_s.fill.solid()
    box_s.fill.fore_color.rgb = ROSE_LIGHT
    box_s.line.color.rgb = CRIMSON

    tb_s = slide5.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.1), Inches(4.9))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    p.text = "The 6 Core Functions & Must-Know Exam Rules:"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CRIMSON

    tips = [
        "1. Protection: First line defense against microbes, UV rays, chemicals, & water loss.",
        "2. Temperature Regulation: Sweating (evaporative cooling) & shivering/vasoconstriction (heat retention).",
        "3. Sensation: Enormous sense organ via cutaneous mechanoreceptors (Pacinian, Meissner, Krause).",
        "4. Excretion: Waste elimination (urea & salts) through sweat gland activity.",
        "5. Vitamin D Synthesis: UV light converts skin precursor to active Vitamin D via liver & kidneys.",
        "6. Absorption: Passive diffusion of lipid-soluble drugs via transdermal patches (e.g. nitroglycerin)."
    ]

    for tip in tips:
        pt = tf_s.add_paragraph()
        pt.text = "✔  " + tip
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = DARK_NAVY
        pt.space_before = Pt(10)

    output_path = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC/Rayne_AP_Module3_Integumentary_System.pptx"
    prs.save(output_path)
    print("Saved A&P PowerPoint to:", output_path)

if __name__ == '__main__':
    build_ap_deck()
