import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    prs = Presentation()
    # Set to widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme colors
    TEAL_DARK = RGBColor(16, 78, 102)     # #104E66
    TEAL_LIGHT = RGBColor(230, 245, 250)  # background
    NAVY = RGBColor(27, 42, 74)         # primary text
    WHITE = RGBColor(255, 255, 255)
    CORAL = RGBColor(220, 80, 60)        # highlight
    GRAY_BG = RGBColor(245, 247, 250)
    CARD_BORDER = RGBColor(200, 215, 225)

    def add_header(slide, title_text, category_text="NCSI1182B • COMMUNICATIONS 1"):
        # Header background shape
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.2))
        header.fill.solid()
        header.fill.fore_color.rgb = TEAL_DARK
        header.line.color.rgb = TEAL_DARK

        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(180, 220, 235)

        # Title text
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
    bg1.fill.fore_color.rgb = TEAL_DARK

    tbox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "NCSI1182B — Communications 1"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(180, 220, 235)

    p2 = tf1.add_paragraph()
    p2.text = "Visual Master Deck: Modules 1 to 3"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Basic Communication • Bridges to Care • Overcoming Barriers"
    p3.font.size = Pt(22)
    p3.font.color.rgb = RGBColor(220, 240, 250)
    p3.space_before = Pt(15)

    p4 = tf1.add_paragraph()
    p4.text = "Prepared for Rayne Moulton | Practical Nursing Study Suite"
    p4.font.size = Pt(16)
    p4.font.italic = True
    p4.font.color.rgb = RGBColor(160, 200, 220)
    p4.space_before = Pt(35)

    # --- SLIDE 2: Module 1 Overview ---
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Module 1: The Core Process of Communication")

    # 3 Cards
    cards_m1 = [
        ("Process & Flow", [
            "Sender encodes message with intent",
            "Transmits through channel (oral, written, nonverbal)",
            "Receiver decodes using context & background",
            "Feedback loop completes comprehension"
        ]),
        ("Types of Communication", [
            "Oral: Spoken speech & words",
            "Written: Symbols, charts, digital notes",
            "Nonverbal: Gestures, facial expression, posture",
            "Metacommunication: Cues that instruct how to interpret"
        ]),
        ("Clinical Impact", [
            "Majority of healthcare errors stem from poor communication",
            "Leading root cause of medication errors & treatment delays",
            "Patient safety is the top priority in nursing care"
        ])
    ]

    for i, (title, bullets) in enumerate(cards_m1):
        left = Inches(0.8 + i * 3.9)
        top = Inches(1.6)
        width = Inches(3.6)
        height = Inches(5.3)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = GRAY_BG
        card.line.color.rgb = CARD_BORDER

        tb = slide2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = TEAL_DARK

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(14)
            pb.font.color.rgb = NAVY
            pb.space_before = Pt(10)

    # --- SLIDE 3: Proxemics & Congruence ---
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Module 1: Proxemics & Message Congruence")

    # Left box: Proxemics
    box_p = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3))
    box_p.fill.solid()
    box_p.fill.fore_color.rgb = GRAY_BG
    box_p.line.color.rgb = CARD_BORDER

    tb_p = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    pt = tf_p.paragraphs[0]
    pt.text = "The 4 Zones of Proxemics (Space)"
    pt.font.size = Pt(18)
    pt.font.bold = True
    pt.font.color.rgb = TEAL_DARK

    prox_data = [
        ("Intimate Space (0 - 45 cm / 18 in):", "Shared with close emotional ties; physical care & procedures."),
        ("Personal Distance (45 cm - 1.2 m / 18 in - 3.5 ft):", "Within arm's reach; ideal for clinical history taking."),
        ("Social Distance (1.2 m - 3.6 m / 3.5 - 12 ft):", "Comfortable for formal & business relationships."),
        ("Public Distance (3.6 m+ / 12 ft+):", "Public settings; non-personal interaction.")
    ]
    for head, desc in prox_data:
        p1 = tf_p.add_paragraph()
        p1.text = "• " + head
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_before = Pt(8)
        p2 = tf_p.add_paragraph()
        p2.text = "  " + desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = NAVY

    # Right box: Congruence
    box_c = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))
    box_c.fill.solid()
    box_c.fill.fore_color.rgb = GRAY_BG
    box_c.line.color.rgb = CARD_BORDER

    tb_c = slide3.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    pt_c = tf_c.paragraphs[0]
    pt_c.text = "Verbal vs Nonverbal Congruence"
    pt_c.font.size = Pt(18)
    pt_c.font.bold = True
    pt_c.font.color.rgb = TEAL_DARK

    cong_bullets = [
        ("Congruent Pattern:", "Verbal words & nonverbal cues match (reinforce each other)."),
        ("Incongruent Pattern:", "Verbal words & body language conflict (e.g., patient says 'No pain' while clutching abdomen)."),
        ("Rule of Dominance:", "When cues conflict, nonverbal body language is perceived as more trustworthy than words!"),
        ("Nursing Role:", "Always point out & explore incongruence gently to uncover real feelings.")
    ]
    for head, desc in cong_bullets:
        p1 = tf_c.add_paragraph()
        p1.text = "• " + head
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_before = Pt(8)
        p2 = tf_c.add_paragraph()
        p2.text = "  " + desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = NAVY

    # --- SLIDE 4: Module 2 Bridges to Effective Communication ---
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Module 2: Key Bridges to Effective Communication")

    bridges = [
        ("Respect", "Address by preferred name. Avoid patronizing terms ('Honey', 'Dear'). Respect patient values."),
        ("Caring", "Roach's 6 C's: Compassion, Competence, Confidence, Conscience, Commitment, Comportment. Swanson's Knowing-Being-Doing."),
        ("Mutuality", "Shared decision-making; nurse & patient work as equal partners on health goals."),
        ("Empowerment", "Provide tools & knowledge for patient self-management. Avoid paternalistic 'I know best' attitude."),
        ("Trust", "Foundation of safety. Built on honesty, consistency, follow-through, and confidentiality."),
        ("Empathy", "Understanding another's feelings nonjudgmentally while maintaining professional boundaries.")
    ]

    for idx, (b_name, b_desc) in enumerate(bridges):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 3.9)
        top = Inches(1.6 + row * 2.7)
        width = Inches(3.6)
        height = Inches(2.4)

        b_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        b_box.fill.solid()
        b_box.fill.fore_color.rgb = GRAY_BG
        b_box.line.color.rgb = CARD_BORDER

        tb = slide4.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = b_name
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = TEAL_DARK

        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = NAVY
        p2.space_before = Pt(6)

    # --- SLIDE 5: Module 3 Barriers to Communication ---
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Module 3: Overcoming Communication Barriers")

    barriers = [
        ("False Reassurance", "Saying 'Everything will be fine' invalidates fears & destroys trust.", "Be honest; offer realistic support based on facts."),
        ("Stereotyping & Bias", "Applying group traits to individuals (stereotype) or personal dislikes (bias).", "Self-awareness & unconditional acceptance without judgment."),
        ("Judgmental Statements", "Adding personal values/opinions to objective facts.", "Provide nonjudgmental holistic care affirming dignity."),
        ("Giving Advice & Opinions", "Telling patients what to do takes away self-determination.", "Use Reflection: 'What options are you considering?'"),
        ("Arguing & Defensiveness", "Challenging patient perceptions denies their reality & breaks rapport.", "Stay calm, listen creatively, maintain respect under stress."),
        ("Patient & Nurse Anxiety", "Distracted thinking, overthinking, and impaired listening.", "Unhurried pace, slow clear speech, active listening, deep breathing.")
    ]

    for idx, (b_name, b_prob, b_sol) in enumerate(barriers):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.6 + row * 1.8)
        width = Inches(5.6)
        height = Inches(1.6)

        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = GRAY_BG
        card.line.color.rgb = CARD_BORDER

        tb = slide5.shapes.add_textbox(left + Inches(0.15), top + Inches(0.1), width - Inches(0.3), height - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = b_name
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = CORAL

        p2 = tf.add_paragraph()
        p2.text = "Barrier: " + b_prob
        p2.font.size = Pt(12)
        p2.font.color.rgb = NAVY

        p3 = tf.add_paragraph()
        p3.text = "Therapeutic Solution: " + b_sol
        p3.font.size = Pt(12)
        p3.font.bold = True
        p3.font.color.rgb = TEAL_DARK

    # --- SLIDE 6: Summary & Exam Tips ---
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Exam Strategy & Clinical Takeaways for Rayne")

    box_s = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    box_s.fill.solid()
    box_s.fill.fore_color.rgb = TEAL_LIGHT
    box_s.line.color.rgb = TEAL_DARK

    tb_s = slide6.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.1), Inches(4.9))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    p.text = "Top NCLEX & Nursing Exam Rules for Communications 1:"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    tips = [
        "Rule 1: Always prioritize Nonverbal Body Language over verbal words when incongruence is present.",
        "Rule 2: Never give False Reassurance ('Everything will be okay'). Always offer honest, data-based support.",
        "Rule 3: Never give Personal Advice ('If I were you...'). Always Reflect questions back to empower the patient.",
        "Rule 4: Avoid patronizing language ('Honey', 'Dear') and paternalistic attitudes ('I know what is best for you').",
        "Rule 5: For anxious patients, reduce environmental stimuli, speak slowly/calmly, and give simple one-step instructions.",
        "Rule 6: Therapeutic communication is ALWAYS goal-directed, patient-centered, and legally/ethically bounded."
    ]

    for tip in tips:
        pt = tf_s.add_paragraph()
        pt.text = "✔  " + tip
        pt.font.size = Pt(15)
        pt.font.bold = True
        pt.font.color.rgb = NAVY
        pt.space_before = Pt(12)

    output_path = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC/Rayne_Communications_1_Modules_1_3.pptx"
    prs.save(output_path)
    print("Saved PowerPoint to:", output_path)

if __name__ == '__main__':
    build_deck()
