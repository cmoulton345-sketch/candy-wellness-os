import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_header_logo_box(doc, doc_id, doc_title):
    header = doc.sections[0].header
    table = header.add_table(rows=1, cols=2, width=Inches(6.5))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Left cell: Logo placeholder
    cell_logo = table.cell(0, 0)
    cell_logo.width = Inches(2.2)
    set_cell_background(cell_logo, "F2F4F7")
    set_cell_margins(cell_logo, top=140, bottom=140, left=140, right=140)
    p_logo = cell_logo.paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_logo = p_logo.add_run("[ INSERT COMPANY LOGO HERE ]")
    run_logo.font.size = Pt(9)
    run_logo.font.bold = True
    run_logo.font.color.rgb = RGBColor(100, 116, 139)
    
    # Right cell: Document metadata
    cell_meta = table.cell(0, 1)
    cell_meta.width = Inches(4.3)
    set_cell_margins(cell_meta, top=100, bottom=100, left=140, right=140)
    p_meta = cell_meta.paragraphs[0]
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_meta_title = p_meta.add_run(f"{doc_title}\n")
    run_meta_title.font.size = Pt(10)
    run_meta_title.font.bold = True
    run_meta_title.font.color.rgb = RGBColor(15, 23, 42)
    
    run_meta_id = p_meta.add_run(f"Doc ID: {doc_id}  |  Rev: 0  |  ISO 45001 Aligned")
    run_meta_id.font.size = Pt(8.5)
    run_meta_id.font.color.rgb = RGBColor(100, 116, 139)
    
    # Add a styled horizontal line below table in doc body
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_after = Pt(12)
    run_sep = p_sep.add_run("―" * 55)
    run_sep.font.color.rgb = RGBColor(203, 213, 225)
    run_sep.font.bold = True

def style_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.name = "Calibri"
        if level == 1:
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(30, 58, 138) # Dark Navy
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout_box(doc, text, title="CRITICAL REQUIREMENT / NOTE"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "FEF3C7") # Warm yellow tint
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    r_title = p.add_run(f"⚠ {title}\n")
    r_title.font.bold = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(180, 83, 9)
    
    r_text = p.add_run(text)
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(120, 53, 15)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_framework_doc():
    doc = docx.Document()
    add_header_logo_box(doc, "FWK-SMS-001", "Safety Documentation Framework Architecture")
    
    style_heading(doc, "1. Executive Summary & Purpose", level=1)
    p = doc.add_paragraph("This document defines the 4-Tier Safety Documentation Framework architecture for our Occupational Health and Safety Management System (OHSMS). The objective is to ensure every safety commitment flows seamlessly from strategic direction down to practical field execution, eliminating ambiguity while fully satisfying ISO 45001:2018 requirements.")
    
    style_heading(doc, "2. The 4-Tier Documentation Hierarchy", level=1)
    
    table = doc.add_table(rows=5, cols=4)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Tier Level", "Document Type", "Core Question & Scope", "Primary Ownership"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)
        
    rows_data = [
        ("Tier 1", "Policy", "WHY we protect people & our commitment\n(ISO 45001 Clause 5.2)", "Senior Management / Safety"),
        ("Tier 2", "Standard", "WHAT specific standards & benchmarks must be met\n(ISO 45001 Clauses 6.1, 6.2, 8.1)", "Safety Department"),
        ("Tier 3", "Guideline (One-Pagers)", "HOW each specific role applies the standard in the field\n(ISO 45001 Clauses 7.2, 7.3)", "Safety Department (with Role SMEs)"),
        ("Tier 4", "Safe Work Practice (SWP)", "HOW we execute work safely on specific equipment / units\n(ISO 45001 Clause 8.1.2)", "Operations / Maintenance (Safety review)")
    ]
    
    for row_idx, data in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            set_cell_margins(cell, 100, 100, 120, 120)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F8FAFC")
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    add_callout_box(doc, "Safety owns the 'What' (Tiers 1-3) and Operations owns the 'How' (Tier 4). SWPs are authored directly by field practitioners and validated by Safety to ensure full compliance with Tier 2 Standards.", "CRITICAL GOVERNANCE PRINCIPLE")
    
    style_heading(doc, "3. ISO 45001:2018 Traceability & Closed-Loop Review", level=1)
    doc.add_paragraph("All documents within this framework are maintained as formal Documented Information (ISO 45001 Clause 7.5). Any field hazard identification, management of change (MOC), or incident investigation automatically triggers a review across all four tiers, ensuring continuous operational improvement.")
    
    doc.save("Safety_Documentation_Framework_Architecture.docx")

def build_policy_doc():
    doc = docx.Document()
    add_header_logo_box(doc, "POL-OHS-001", "Occupational Health & Safety Policy")
    
    style_heading(doc, "Occupational Health & Safety (OH&S) Policy", level=1)
    
    p = doc.add_paragraph()
    p.add_run("At ").font.size = Pt(11)
    r_co = p.add_run("[ INSERT COMPANY NAME HERE ]")
    r_co.font.bold = True
    r_co.font.size = Pt(11)
    p.add_run(", people are our most valuable resource. We are committed to providing a safe, healthy, and incident-free work environment for all employees, contractors, visitors, and community members across all operations.")
    
    style_heading(doc, "Core Commitments (ISO 45001 Clause 5.2)", level=2)
    commitments = [
        "Eliminating Hazards & Reducing Risks: Systematically identifying occupational hazards and mitigating risks to prevent work-related injury and ill health.",
        "Full Legal & Compliance Rigor: Complying with or exceeding all applicable regulatory requirements (WorkSafe, National Building Code, CSA standards) and binding agreements.",
        "Worker Consultation & Participation: Actively engaging workers and their representatives at all levels in the design, implementation, and evaluation of our safety management system.",
        "Continual Improvement: Regularly monitoring performance metrics, conducting audits, and updating controls to foster an evolving, resilient safety culture."
    ]
    for c in commitments:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(c.split(":")[0] + ":")
        r.font.bold = True
        r.font.size = Pt(10)
        r2 = p.add_run(c.split(":")[1])
        r2.font.size = Pt(10)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(16)
    
    # Sign-off block
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in range(2):
        for c in range(2):
            cell = table.cell(r, c)
            set_cell_margins(cell, 120, 120, 120, 120)
            set_cell_background(cell, "F8FAFC")
            
    table.cell(0, 0).paragraphs[0].add_run("Approved By: ___________________________\nChief Executive Officer / Site Director").font.bold = True
    table.cell(0, 1).paragraphs[0].add_run("Endorsed By: ___________________________\nVP Operations / Safety Manager").font.bold = True
    table.cell(1, 0).paragraphs[0].add_run("Effective Date: [ YYYY-MM-DD ]")
    table.cell(1, 1).paragraphs[0].add_run("Review Cadence: Annual")
    
    doc.save("POL-OHS-001_Safety_Policy_Template.docx")

def build_standard_doc():
    doc = docx.Document()
    add_header_logo_box(doc, "STD-CS-001", "Standard: Confined Space Entry & Atmospheric Monitoring")
    
    style_heading(doc, "1. Purpose & Scope", level=1)
    doc.add_paragraph("This Standard defines the mandatory technical and procedural controls required to protect workers entering or operating within confined spaces across all facility assets. It fulfills ISO 45001 Clauses 6.1 (Risk Assessment) and 8.1 (Operational Control).")
    
    style_heading(doc, "2. Mandatory Requirements & Controls", level=1)
    
    reqs = [
        ("Permit Authorization", "No personnel shall enter a confined space without an approved, active Confined Space Entry Permit posted at the primary access point."),
        ("Atmospheric Testing", "Pre-entry atmospheric testing must occur within 20 minutes of entry using a calibrated 4-gas monitor (O2, LEL, H2S, CO). Continuous atmospheric monitoring is mandatory during occupancy."),
        ("Dedicated Standby Person", "A qualified Standby Person must remain stationed outside the entrance at all times during occupancy with no concurrent secondary duties."),
        ("Staged Rescue Plan", "A specific rescue plan must be established prior to entry, with extraction equipment (tripod, winch, harness, SCBA) staged and verified operable.")
    ]
    
    for title, desc in reqs:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(f"{title}: ")
        r.font.bold = True
        r.font.size = Pt(10)
        p.add_run(desc).font.size = Pt(10)
        
    add_callout_box(doc, "If atmospheric testing shows O2 < 19.5% or > 23.0%, LEL > 0%, or toxic gases above occupational exposure limits, STOP WORK immediately and evacuate.", "ATMOSPHERIC STOP WORK THRESHOLD")
    
    style_heading(doc, "3. Roles & Accountability Matrix", level=1)
    table = doc.add_table(rows=4, cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Role", "Mandatory Accountability"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 100, 100, 120, 120)
        r = cell.paragraphs[0].add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    roles_data = [
        ("Supervisor", "Verify physical positive isolations (LOTO), review and authorize entry permit, confirm rescue readiness."),
        ("Standby Person", "Maintain continuous head count, monitor atmospheric alarm status, initiate emergency rescue protocols if needed."),
        ("Entrant", "Inspect personal harness/monitor, comply with permit instructions, evacuate immediately upon standby alarm or order.")
    ]
    for row_idx, (role, acc) in enumerate(roles_data, start=1):
        cell_r = table.cell(row_idx, 0)
        cell_a = table.cell(row_idx, 1)
        set_cell_margins(cell_r, 100, 100, 120, 120)
        set_cell_margins(cell_a, 100, 100, 120, 120)
        if row_idx % 2 == 0:
            set_cell_background(cell_r, "F8FAFC")
            set_cell_background(cell_a, "F8FAFC")
        cell_r.paragraphs[0].add_run(role).font.bold = True
        cell_a.paragraphs[0].add_run(acc)
        
    doc.save("STD-CS-001_Confined_Space_Standard_Template.docx")

def build_guideline_one_pager():
    doc = docx.Document()
    add_header_logo_box(doc, "GDL-CS-SUP-001", "Guideline One-Pager: Confined Space Supervisor")
    
    style_heading(doc, "FIELD ACTION GUIDE: CONFINED SPACE SUPERVISOR", level=1)
    doc.add_paragraph("Target Role: Front-Line Supervisor / Permit Issuer  |  Parent Standard: STD-CS-001").runs[0].font.italic = True
    
    style_heading(doc, "✔ Pre-Entry Verification Checklist", level=2)
    checks = [
        "Verify all energy sources are positively isolated per LOTO procedure (blinds/blanks/disconnects verified).",
        "Inspect and verify calibration dates on all 4-gas atmospheric monitors.",
        "Conduct pre-job toolbox talk with Entrants and Standby Person; review specific hazards and rescue plan.",
        "Verify rescue equipment (tripod, winch, extraction lines, SCBA) is staged at the hatch and fully functional.",
        "Sign and post the Confined Space Permit at the physical entry point."
    ]
    for c in checks:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run("  [   ]   ")
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138)
        p.add_run(c).font.size = Pt(9.5)
        
    style_heading(doc, "🛑 Mandatory Stop-Work Triggers", level=2)
    stops = [
        "Any atmospheric alarm activation on personal or area gas detectors.",
        "Standby Person must leave their post without a certified replacement present.",
        "Loss of ventilation airflow or power loss to extraction blowers.",
        "Unanticipated chemical odors, sludge disturbance, or ingress of liquids."
    ]
    for s in stops:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run("  🛑   ")
        p.add_run(s).font.size = Pt(9.5)
        
    add_callout_box(doc, "Life Saving Rules Applicable: LSR-01 (Confined Space) & LSR-02 (Energy Isolation). Violations result in immediate stand-down.", "LIFE SAVING RULES MANDATE")
    
    doc.save("GDL-CS-SUP-001_Supervisor_Guideline_OnePager.docx")

def build_swp_doc():
    doc = docx.Document()
    add_header_logo_box(doc, "SWP-AGRU-P101A-001", "SWP: Taking Amine Pump P-101A Offline for Seal Replacement")
    
    style_heading(doc, "1. Task & Equipment Overview", level=1)
    table = doc.add_table(rows=3, cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Unit / Area:", "Gas Pretreatment — Warm End (AGRU)"),
        ("Equipment Tag:", "Amine Reflux Pump P-101A"),
        ("Parent Standards:", "STD-CS-001 (Confined Space), STD-EI-002 (LOTO), STD-H2S-001 (H2S Safety)")
    ]
    for r_idx, (k, v) in enumerate(meta):
        c0 = table.cell(r_idx, 0)
        c1 = table.cell(r_idx, 1)
        set_cell_margins(c0, 80, 80, 100, 100)
        set_cell_margins(c1, 80, 80, 100, 100)
        set_cell_background(c0, "F1F5F9")
        c0.paragraphs[0].add_run(k).font.bold = True
        c1.paragraphs[0].add_run(v)
        
    style_heading(doc, "2. Required Personal Protective Equipment (PPE)", level=1)
    doc.add_paragraph("Mandatory PPE: H2S Personal Monitor, Amine-Rated Splash Goggles, Face Shield, Chemical Apron, Butyl/Nitrile Gloves, Steel-Toe Boots, Hard Hat.")
    
    style_heading(doc, "3. Step-by-Step Operational Procedure", level=1)
    steps = [
        ("Notify & Coordinate", "Contact Control Room Operator (CRO) and confirm standby pump P-101B is online, primed, and taking the full amine circulation load without pressure spikes."),
        ("Isolate Discharge", "Slowly close discharge block valve XV-101A over a 2-minute duration to prevent water hammer on the column reflux line."),
        ("Isolate Suction", "Close suction block valve XV-101A-S firmly. Verify local pressure gauge shows 0 psig differential across suction line."),
        ("Apply LOTO", "Perform positive electrical lockout on P-101A motor breaker at MCC Substation 2. Apply multi-lock hasps and tags on both suction and discharge handwheels per STD-EI-002."),
        ("Depressurize & Drain", "Connect closed-loop drain hose to pump casing bleed valve. Slowly open bleed valve to drain residual amine into closed hazardous drain header. Verify zero residual liquid."),
        ("Flush & Clean", "Connect demineralized utility water flush to casing vent. Flush casing for 15 minutes until effluent is clear and pH tested neutral."),
        ("Handover to Maintenance", "Perform joint field walkdown with Maintenance Lead. Sign Permit to Work and authorize mechanical disconnection.")
    ]
    
    for idx, (title, detail) in enumerate(steps, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r_num = p.add_run(f"Step {idx}. {title}: ")
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(30, 58, 138)
        p.add_run(detail).font.size = Pt(9.5)
        
    add_callout_box(doc, "Caution: Amine solution under pressure can release H2S pockets during initial bleed. Ensure respiratory protection or SCBA is immediately staged during initial casing bleed.", "HIGH HAZARD WARNING")
    
    doc.save("SWP-AGRU-P101A-001_Safe_Work_Practice_Template.docx")

if __name__ == "__main__":
    build_framework_doc()
    build_policy_doc()
    build_standard_doc()
    build_guideline_one_pager()
    build_swp_doc()
    print("All 5 Word documents successfully generated.")
