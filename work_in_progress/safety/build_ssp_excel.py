import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_ssp_excel():
    base = os.path.dirname(os.path.abspath(__file__))
    wb = Workbook()
    
    # Common styles
    tb = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
    hf = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid") # Dark Navy
    hn = Font(bold=True, size=10, color="FFFFFF")
    ha = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    rc = {
        "Critical": PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid"),
        "High": PatternFill(start_color="FF8C00", end_color="FF8C00", fill_type="solid"),
        "Medium": PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid"),
        "Low": PatternFill(start_color="32CD32", end_color="32CD32", fill_type="solid")
    }
    rf = {
        "Critical": Font(bold=True, color="FFFFFF", size=10),
        "High": Font(bold=True, size=10),
        "Medium": Font(bold=True, size=10),
        "Low": Font(bold=True, color="FFFFFF", size=10)
    }

    # ==========================================
    # Sheet 1: Safety-Sensitive Positions (SSP)
    # ==========================================
    ws1 = wb.active
    ws1.title = "Safety-Sensitive Positions"
    
    # Title Blocks
    ws1.merge_cells("A1:G1")
    c = ws1["A1"]
    c.value = "SAFETY-SENSITIVE POSITIONS (SSP) REGISTRY — LNG Facility (Squamish, BC)"
    c.font = Font(bold=True, size=14, color="FFFFFF")
    c.fill = hf
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 36
    
    ws1.merge_cells("A2:G2")
    c = ws1["A2"]
    c.value = "WorkSafeBC Part 3/23 Aligned | BCER Reg Compliant | Canadian Model D&A Zero Tolerance | 12-Hr Shift & FRMS Controlled"
    c.font = Font(italic=True, size=10, color="FFFFFF")
    c.fill = PatternFill(start_color="2E5090", end_color="2E5090", fill_type="solid")
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[2].height = 22
    
    # Headers
    cols = [
        ("SSP ID", 10),
        ("Position Title", 30),
        ("Key Phase", 22),
        ("Critical Safety Responsibilities", 45),
        ("Critical Barriers / Risk IDs Owned", 32),
        ("Mandatory Competency & Certifications", 45),
        ("Fitness & Medical Requirements (FRMS)", 45)
    ]
    
    for ci, (cn, cw) in enumerate(cols, 1):
        c = ws1.cell(row=3, column=ci, value=cn)
        c.font = hn
        c.fill = hf
        c.alignment = ha
        c.border = tb
        ws1.column_dimensions[get_column_letter(ci)].width = cw
    ws1.row_dimensions[3].height = 32
    
    ssp_data = [
        ("SSP-001", "Control Room Operator (DCS Panel Operator)", "Commissioning & Operations",
         "Monitors safe operating limits (SOLs); manages alarm rationalization; executes Emergency Shutdown (ESD) protocols; oversees plant status.",
         "CRIT-03 (Bypasses)\nOPS-CRIT-05 (Alarm Flooding)\nOPS-CRIT-06 (Hydrates)",
         "• Certified Operator Training Simulator (OTS) program\n• ISA-18.2 Alarm Management training\n• Annual ESD simulation certification",
         "• Mandatory pre-employment & post-incident D&A testing\n• Visual/hearing acuity check\n• Strict cognitive fatigue limit audits"),
         
        ("SSP-002", "Operations Director / Shift Charge Engineer", "Transition & Operations",
         "Ultimate shift authority; final approver of critical safety bypasses (T-MOCs) and initial gas introduction; directs emergency shut-ins.",
         "CRIT-02 (First Gas)\nREG-01 (Leave to Open)\nOPS-CRIT-07 (Turnarounds)",
         "• P.Eng registration or equivalent technical diploma\n• ICS 300 (Incident Command System) certification\n• 10+ years LNG operations experience",
         "• Mandatory pre-employment & post-incident D&A testing\n• Periodic fitness-for-duty medical clearance\n• Executive emergency response clearance"),
         
        ("SSP-003", "SIMOPS Coordinator", "Commissioning & Transition",
         "Manages physical and temporal boundaries between construction work and live commissioning/startup loops; signs interface permits.",
         "CRIT-01 (SIMOPS)\nLOTO-01 (LOTO transition)\nLIFT-01 (Critical Lifts)",
         "• Prime Contractor Coordinator training (WorkSafeBC)\n• Hazard Identification & Risk Assessment (HIRA)\n• Advanced Permit-to-Work (PTW) issuer cert",
         "• Mandatory pre-employment & post-incident D&A testing\n• Physical endurance for active construction walkdowns"),
         
        ("SSP-004", "Permit Issuer / Area Authority", "All Phases",
         "Performs physical gas testing (LEL, O2, toxic gas); validates LOTO isolation points in the field; issues high-risk work permits.",
         "LOTO-01 (LOTO)\nCSE-01 (Confined Space)\nUTIL-01 (Nitrogen)",
         "• Certified Gas Tester (CSA Z1002 compliant)\n• Master Isolation Authority certification\n• Root Cause Analysis (RCA) basic training",
         "• Pre-employment & post-incident D&A testing\n• Physical ability to walk process structures & pipe racks"),
         
        ("SSP-005", "Outside Field Operator (Liquefaction/Storage/Marine)", "Transition & Operations",
         "Executes manual valving, LOTO box locking, line walks, and cryogenic cool-down tracking; monitors physical plant loops.",
         "OPS-02 (Thermal Shock)\nOPS-CRIT-03 (Rollover)\nOPS-CRIT-04 (Embrittlement)",
         "• Power Engineering certification (Class 3 or 4)\n• Site-specific SOP and line-walk validation\n• Cryogenic safety and hazard handling",
         "• Pre-employment & post-incident D&A testing\n• SCBA user medical fit test\n• Confined space rescue capability check"),
         
        ("SSP-006", "Marine Terminal Supervisor / Jetty Operator", "Transition & Operations",
         "Manages LNG carrier berthing, loading arm connection, mooring tension, seawater curtain flows, and Emergency Release Systems (ERS).",
         "MAR-01 (Loading Arms)\nOPS-CRIT-01 (RPT on Water)\nOPS-CRIT-08 (Jetty Collision)",
         "• Transport Canada marine terminal certification\n• ERS/ERC system test and manual override training\n• Water-activated PFD & rescue boat coxswain cert",
         "• Pre-employment & post-incident D&A testing\n• Water rescue fitness and swimming clearance"),
         
        ("SSP-007", "High-Voltage Electrical Technician", "Commissioning & Maintenance",
         "Performs high-voltage switching, utility energization, substation maintenance, and sets up arc flash boundaries.",
         "UTIL-02 (Arc Flash / HV)\nLOTO-01 (LOTO)",
         "• Red Seal Electrical Journeyman (or equivalent)\n• CSA Z462 Electrical Safety training\n• Certified High-Voltage Switching Operator",
         "• Pre-employment & post-incident D&A testing\n• Color-blindness screening (for wiring diagnostics)"),
         
        ("SSP-008", "Instrumentation & Control (I&C) Technician", "Commissioning & Maintenance",
         "Calibrates fixed fire & gas (F&G) detectors; tests ESD valves; programs DCS interlocks and safety-instrumented systems (SIS).",
         "CRIT-03 (Bypasses)\nCHEM-01 (Ammonia Leak)\nOPS-CRIT-05 (SIS)",
         "• Instrumentation Journeyman certification\n• TUV Functional Safety Engineer certification (preferred)\n• Safety Instrumented Systems (SIS) standard training",
         "• Pre-employment & post-incident D&A testing\n• High-precision fine motor skill validation"),
         
        ("SSP-009", "Emergency Response Team (ERT) Leader", "All Phases",
         "Directs industrial fire, cryogenic vapor cloud dispersion, ammonia leak containment, and marine search and rescue.",
         "CHEM-01 (Ammonia)\nOPS-CRIT-02 (BLEVE)\nWAT-01 (Falls Over Water)",
         "• NFPA 1081 (Industrial Fire Brigade Member)\n• NFPA 472 / 1072 (Hazardous Materials Technican)\n• Advanced First Aid / First Responder",
         "• Annual high-rigor cardiovascular & physical fit test\n• Claustrophobia/SCBA entry medical clearance\n• Pre-employment & post-incident D&A testing")
    ]
    
    for ri, row in enumerate(ssp_data, 4):
        for ci, val in enumerate(row, 1):
            c = ws1.cell(row=ri, column=ci, value=val)
            c.font = Font(size=10, bold=(ci==1 or ci==2))
            c.alignment = Alignment(vertical="top", horizontal=("center" if ci==1 else "left"), wrap_text=True)
            c.border = tb
        ws1.row_dimensions[ri].height = 75
        
    ws1.freeze_panes = "A4"
    ws1.auto_filter.ref = f"A3:G{3+len(ssp_data)}"

    # ==========================================
    # Sheet 2: Risk Mapping & Prefix Legend
    # ==========================================
    ws2 = wb.create_sheet("Prefix Legend & Risk Mapping")
    ws2.merge_cells("A1:D1")
    ws2["A1"].value = "RISK ID NOMENCLATURE & PREFIX LEGEND — Mapped to LNG Registers"
    ws2["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws2["A1"].fill = hf
    ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws2.row_dimensions[1].height = 36
    
    legend_cols = [("Prefix", 15), ("Hazard Category", 32), ("Description & Examples", 55), ("Mapped Register", 25)]
    for ci, (cn, cw) in enumerate(legend_cols, 1):
        c = ws2.cell(row=3, column=ci, value=cn)
        c.font = hn
        c.fill = hf
        c.alignment = ha
        c.border = tb
        ws2.column_dimensions[get_column_letter(ci)].width = cw
    ws2.row_dimensions[3].height = 28
    
    legend_data = [
        ("CRIT", "Critical SIMOPS & Commissioning", "Bypasses, first gas introduction, SIMOPS ignition sources.", "Transition Register"),
        ("LOTO", "Lockout / Tagout", "Energy isolations, valve/electrical boundary locks.", "Transition Register"),
        ("CSE", "Confined Space Entry", "Multi-jurisdictional confined spaces, vessel entries.", "Transition Register"),
        ("WAT", "Over-Water Work", "Jetty constructions, falls over marine environments.", "Transition Register"),
        ("UTIL", "Purging & Utilities", "Nitrogen asphyxiation, high-voltage substations.", "Transition Register"),
        ("CHEM", "Hazardous Chemicals", "Ammonia refrigerant systems, chemical handling.", "Transition Register"),
        ("MAR", "Marine Terminal Operations", "Loading arm maneuvers, ship-to-shore vessel lines.", "Transition Register"),
        ("TS", "Pressure Testing", "Hydrostatic/pneumatic line ruptures.", "Transition Register"),
        ("ENV", "Environmental Compliance", "Underwater noise, flaring limits, emission controls.", "Transition Register"),
        ("OPS", "Commissioning & Operations", "Thermal shock (banana effect), CUI piping failures.", "Transition Register"),
        ("REG", "Regulatory Compliance", "Leave to Open (LTO) approvals, BCER conditions.", "Transition Register"),
        ("LIFT", "SIMOPS Lifting Operations", "Heavy module rigging, crane safety, drops.", "Transition Register"),
        ("VEH", "Mobile Equipment & Traffic", "Site traffic, pedestrian walkways, backing safety.", "Transition Register"),
        ("OPS-CRIT", "Continuous Process Safety", "Rollover, BLEVE, RPT, alarm floods, ship collisions.", "Operations Register")
    ]
    
    for ri, row in enumerate(legend_data, 4):
        for ci, val in enumerate(row, 1):
            c = ws2.cell(row=ri, column=ci, value=val)
            c.font = Font(size=10, bold=(ci==1 or ci==4))
            c.alignment = Alignment(vertical="top", horizontal=("center" if ci==1 else "left"), wrap_text=True)
            c.border = tb
        ws2.row_dimensions[ri].height = 26
    ws2.freeze_panes = "A4"

    # ==========================================
    # Sheet 3: FRMS & D&A Protocols
    # ==========================================
    ws3 = wb.create_sheet("FRMS & Fitness Protocols")
    ws3.merge_cells("A1:D1")
    ws3["A1"].value = "FITNESS-FOR-DUTY & FATIGUE RISK MANAGEMENT SYSTEM (FRMS)"
    ws3["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws3["A1"].fill = hf
    ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws3.row_dimensions[1].height = 36
    
    frms_cols = [("Protocol Category", 24), ("Requirement Element", 32), ("Operational Standard / Mandatory Limit", 50), ("Compliance & Audit Mechanism", 35)]
    for ci, (cn, cw) in enumerate(frms_cols, 1):
        c = ws3.cell(row=3, column=ci, value=cn)
        c.font = hn
        c.fill = hf
        c.alignment = ha
        c.border = tb
        ws3.column_dimensions[get_column_letter(ci)].width = cw
    ws3.row_dimensions[3].height = 28
    
    frms_data = [
        ("Shift & Hours Limits", "Maximum Shift Length", "Strict 12-hour ceiling for all SSP personnel (excluding authorized plant shut-ins).", "Automated time card & electronic gate audit"),
        ("Shift & Hours Limits", "Minimum Rest Period", "Mandatory minimum 11 hours of continuous rest between consecutive shifts.", "Automated time card interlock"),
        ("Shift & Hours Limits", "Max Consecutive Shifts", "Max 4 night shifts (12-hr) OR max 6 day shifts (12-hr). Mandatory 3 days rest post-nights.", "Shift schedule compliance tracking"),
        ("Shift & Hours Limits", "Weekly Overtime Cap", "Absolute cap of 60 hours worked per 7-day period. Requires Ops Manager approval beyond 50h.", "Weekly hours exceedance KPI"),
        ("Drug & Alcohol Policy", "Zero-Tolerance Threshold", "Zero tolerance for alcohol, recreational cannabis, or illicit substances while on site/floatel.", "Pre-employment & site gate checks"),
        ("Drug & Alcohol Policy", "Mandatory Testing Triggers", "Pre-placement, Reasonable Cause, Random testing, and mandatory within 2 hours post-incident.", "Third-party D&A testing provider"),
        ("Drug & Alcohol Policy", "Prescription Medications", "Mandatory declaration to Occupational Health Nurse of any meds with drowsiness/alertness warnings.", "Confidential OHN medical registry"),
        ("Cognitive Alertness", "Shift Start FLHA Integration", "Daily self-assessment of sleep duration (>6 hours target) and mental alertness prior to work.", "Daily FLHA card verification"),
        ("Cognitive Alertness", "DCS Screen Rotation", "Control room operators must rotate screens or take brief visual stand-downs every 4 hours.", "Shift Supervisor walkdown check"),
        ("Cognitive Alertness", "Peer Checkpoints", "Supervisors conduct face-to-face alertness checks at the 6-hour mark of every 12-hour shift.", "Documented supervisory log")
    ]
    
    for ri, row in enumerate(frms_data, 4):
        for ci, val in enumerate(row, 1):
            c = ws3.cell(row=ri, column=ci, value=val)
            c.font = Font(size=10, bold=(ci==1 or ci==2))
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = tb
        ws3.row_dimensions[ri].height = 32
    ws3.freeze_panes = "A4"

    out = os.path.join(base, "LNG_LNG_Safety_Sensitive_Positions_Registry.xlsx")
    wb.save(out)
    print(f"SSP Registry Excel saved successfully: {out}")

if __name__ == "__main__":
    build_ssp_excel()
