import json,os
base=os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base,"cri_data_part1.json")) as f: d1=json.load(f)
with open(os.path.join(base,"cri_data_part2.json")) as f: d2=json.load(f)
all_data=d1+d2

# Map ESC Life Saving Rules + SIF flag to existing entries
lsr_map={
    "CRI-002":"LSR-01: Confined Space; LSR-03: Work Authorization",
    "CRI-004":"LSR-04: Safety Controls",
    "CRI-005":"LSR-02: Energy Isolation; LSR-04: Safety Controls",
    "CRI-008":"LSR-03: Work Authorization; LSR-04: Safety Controls",
    "CRI-009":"LSR-04: Safety Controls",
    "CRI-011":"LSR-04: Safety Controls",
    "CRI-012":"LSR-04: Safety Controls",
    "CRI-013":"LSR-04: Safety Controls",
    "CRI-014":"LSR-04: Safety Controls",
    "CRI-017":"LSR-02: Energy Isolation",
    "CRI-018":"LSR-01: Confined Space; LSR-03: Work Authorization",
    "CRI-019":"LSR-07: Hot Work; LSR-03: Work Authorization",
    "CRI-020":"LSR-05: Working at Height",
    "CRI-021":"LSR-02: Energy Isolation; LSR-01: Confined Space; LSR-09: Safe Mechanical Lifting",
    "CRI-022":"LSR-02: Energy Isolation",
    "CRI-024":"LSR-02: Energy Isolation; LSR-04: Safety Controls",
    "CRI-025":"LSR-04: Safety Controls",
}
sif_all=["CRI-002","CRI-004","CRI-005","CRI-006","CRI-008","CRI-009","CRI-010","CRI-011","CRI-012","CRI-013","CRI-014","CRI-015","CRI-016","CRI-017","CRI-018","CRI-019","CRI-020","CRI-021","CRI-022","CRI-023","CRI-024","CRI-025","CRI-026","CRI-027","CRI-028","CRI-029"]

# KPIs per entry type
kpi_map_area={
    "Gas Pretreatment":"Tier 1/2 LOPC count; H2S detector response time; PSV test compliance %",
    "Liquefaction":"Tier 1/2 LOPC count; Compressor availability %; Unplanned shutdown frequency",
    "Condensate":"Tier 1/2 LOPC count; Static grounding verification compliance %",
    "Floating Storage":"Tier 1/2 LOPC count; BOG compressor availability %; Marine loading ERS test compliance",
    "Plant-Wide":"ESD proof test compliance %; LOTO audit pass rate; Overdue corrective actions count; PSI reporting rate; Life Saving Rule violation count",
    "Remote Site":"Wildlife incident count; Medevac response time; Severe weather stand-down compliance %",
}

for i,rec in enumerate(all_data):
    cid=f"CRI-{i+1:03d}"
    rec["LSR"]=lsr_map.get(cid,"N/A")
    rec["SIF"]="YES" if cid in sif_all else "NO"
    area=rec["Area"]
    kpi="ESD proof test %; LOTO audit %; Overdue CAs; PSI rate"
    for k,v in kpi_map_area.items():
        if k in area: kpi=v; break
    rec["KPI"]=kpi

# Add new entries for missing ESC Life Saving Rules
new_entries=[
    {"Area":"Plant-Wide","Task":"Driving / Mobile Equipment Operations (Site Roads, Access Routes)","Role":"All Personnel","Phase":"Normal Ops","Hazards":"Vehicle collision on narrow site/access roads; Rollover on steep terrain; Pedestrian strike; Wildlife-vehicle collision; Fatigue-impaired driving (7/7 or 4/4 shift rotation)","Consequence":"Fatality from collision/rollover; Serious injury; Wildlife mortality","Pre-Risk":"High","Controls":"Journey management plan; Speed limits enforced (GPS monitoring); Seatbelt policy (zero tolerance); Fit-for-duty checks (fatigue/impairment); Defensive driving training; Vehicle pre-trip inspection; Restricted cell phone use; Winter tire/chain requirements","Competency":"Defensive driving certification; Winter driving skills; Vehicle pre-trip inspection; Journey management planning","Training":"Defensive driving course (Energy Safety Canada); Winter driving practical; Fatigue management awareness; Annual recertification","Residual":"Medium","Reg Ref":"ESC Life Saving Rules; WorkSafeBC OHS Reg Part 16; Motor Vehicle Act (BC)","LSR":"LSR-06: Driving","SIF":"YES","KPI":"Vehicle incident rate; Seatbelt compliance %; Journey management compliance %"},
    {"Area":"Plant-Wide","Task":"Fit for Duty Management (Fatigue, Impairment, Mental Fitness)","Role":"All Personnel","Phase":"Normal Ops","Hazards":"Fatigue from 7/7 or 4/4 shift rotation; Alcohol/drug impairment; Mental health/stress (remote site isolation); Sleep deprivation during startup/turnaround extended shifts","Consequence":"Human error leading to process upset/injury; Impaired emergency response; Fatality from fatigue-related incident","Pre-Risk":"High","Controls":"Fit-for-duty policy (drug & alcohol testing - pre-employment, random, post-incident); Fatigue risk management system (FRMS) aligned to API RP 755; Maximum hours-of-work limits; Peer-to-peer fatigue observation program; Employee assistance program (EAP); Mental health resources on floatel","Competency":"Fatigue recognition (self and peers); Drug & alcohol policy awareness; Mental health first aid; Reporting procedures","Training":"Fit-for-duty orientation (all new hires); Fatigue management awareness (annual); Mental health first aid (designated personnel); Supervisor: Impairment recognition","Residual":"Medium","Reg Ref":"ESC Life Saving Rules (LSR-08); API RP 755; WorkSafeBC OHS Reg; Canadian Human Rights Act","LSR":"LSR-08: Fit for Duty","SIF":"YES","KPI":"Random D&A test compliance %; Hours-of-work exceedance count; EAP utilization rate"},
    {"Area":"Plant-Wide","Task":"Line of Fire Awareness (Struck-By, Caught-Between, Pressure Release)","Role":"All Personnel","Phase":"Normal Ops","Hazards":"Struck by pressurized fluid/gas release; Caught between moving equipment; Struck by falling object; Whip from tensioned lines/hoses; Ejection of valve components under pressure","Consequence":"Fatality; Amputation; High-pressure injection injury; Traumatic injury","Pre-Risk":"Critical","Controls":"Line-of-fire awareness integrated into all JSAs/task risk assessments; Exclusion zones during pressure testing; Barricading during overhead work; Restraint on pressurized hoses; Stand-clear zones during valve operation; Dropped object prevention (tool tethering, barricade nets)","Competency":"Line-of-fire hazard recognition; JSA/task risk assessment; Exclusion zone setup; Pressure testing safety","Training":"Line-of-fire awareness module (all new hires); JSA/TRA practical training; Toolbox talks (monthly rotation); Annual refresher","Residual":"Medium","Reg Ref":"ESC Life Saving Rules (LSR-10); WorkSafeBC OHS Reg","LSR":"LSR-10: Line of Fire","SIF":"YES","KPI":"Line-of-fire near-miss reporting rate; JSA completion compliance %"},
    {"Area":"Plant-Wide","Task":"Safe Mechanical Lifting (Cranes, Rigging, Overhead Lifts)","Role":"Maintenance Tech","Phase":"Normal Ops / Turnaround","Hazards":"Dropped load (crusher/fatality); Crane tip-over; Rigging failure (sling/shackle); Personnel under suspended load; Boom contact with overhead power lines or structures; Wind load on suspended equipment","Consequence":"Fatality from dropped load; Crush injury; Electrocution from power line contact","Pre-Risk":"Critical","Controls":"Lift plan for all critical lifts (>80% crane capacity or near infrastructure); Certified crane operator and rigger; Pre-lift inspection of all rigging gear; No personnel under suspended load (zero tolerance); Wind speed limits for lifting; Spotter/signal person for blind lifts; Exclusion zone barricading","Competency":"Crane operator certification; Rigger certification; Lift planning; Rigging gear inspection; Signal person training","Training":"Crane operator certification (provincial); Rigger training and certification; Lift planning course; Annual practical assessment","Residual":"Medium","Reg Ref":"ESC Life Saving Rules (LSR-09); WorkSafeBC OHS Reg Part 15; CSA Z150","LSR":"LSR-09: Safe Mechanical Lifting","SIF":"YES","KPI":"Critical lift plan compliance %; Rigging gear inspection compliance %; Lifting near-miss rate"},
    {"Area":"Plant-Wide","Task":"Bypassing/Overriding Safety Controls (SIS Bypass, Alarm Suppression, Interlock Defeat)","Role":"Operator","Phase":"Normal Ops / Startup","Hazards":"Loss of safety protection layer; Undetected hazardous condition escalation; Alarm flood masking critical alarms; Normalized deviation (drift into failure)","Consequence":"Major process safety event (explosion, fire, toxic release); Multiple fatalities; Regulatory enforcement action","Pre-Risk":"Critical","Controls":"Safety control bypass/override authorization procedure (senior management approval); Time-limited bypass with compensating measures documented; Bypass register visible in control room; Alarm rationalization program (ISA-18.2); Independent bypass audit (quarterly); Management of Change for any permanent alteration","Competency":"SIS/SIL understanding; Bypass authorization process; Alarm management principles; Compensating measure identification","Training":"SIS bypass management procedure training; Alarm management awareness; Tabletop: Scenario with multiple bypasses active; Annual refresher","Residual":"High","Reg Ref":"ESC Life Saving Rules (LSR-04); IEC 61511; ISA-18.2; WorkSafeBC","LSR":"LSR-04: Safety Controls","SIF":"YES","KPI":"Active SIS bypass count; Bypass duration exceedance count; Standing alarm count; Alarm rate per operator per hour"},
    {"Area":"Plant-Wide","Task":"Work Authorization / Permit to Work System","Role":"All Personnel","Phase":"Normal Ops / Turnaround","Hazards":"Uncontrolled simultaneous activities (SIMOPS); Work in wrong location; Work without adequate isolation; Permit-to-work non-compliance; Permit conflicts during turnaround","Consequence":"Fatality from uncoordinated activities; Fire/explosion from inadequate isolation; Injury from concurrent incompatible work","Pre-Risk":"Critical","Controls":"Integrated permit-to-work system (electronic preferred); SIMOPS coordination procedure with single point of accountability; Permit cross-referencing for conflicts; Site verification before work start; Permit audit program; Turnaround SIMOPS planning meetings (daily)","Competency":"PTW system operation; SIMOPS awareness; Permit conflict identification; Cross-craft coordination","Training":"PTW system training (all permit holders and performers); SIMOPS coordination training (supervisors); Practical: Permit completion + site verification exercise; Annual refresher","Residual":"Medium","Reg Ref":"ESC Life Saving Rules (LSR-03); WorkSafeBC OHS Reg; OGP Report 394","LSR":"LSR-03: Work Authorization","SIF":"YES","KPI":"PTW audit pass rate %; SIMOPS conflict count; Permit close-out compliance %"},
    {"Area":"Plant-Wide","Task":"First Nations Cultural Safety & Environmental Protocol Compliance","Role":"All Personnel","Phase":"Normal Ops","Hazards":"Violation of Squamish Nation cultural site protections; Unauthorized disturbance of archaeological/heritage resources; Non-compliance with SNEAA conditions; Damage to culturally significant species/habitat","Consequence":"Regulatory shutdown (breach of EA conditions); Legal action; Loss of social license to operate; Relationship damage with Squamish Nation","Pre-Risk":"High","Controls":"Squamish Nation Environmental Assessment Agreement (SNEAA) - 25 binding conditions; Cultural awareness training mandatory for all personnel; Archaeological chance-find procedure; Squamish Nation environmental monitors on site; Cultural site buffer zones with signage; Bi-annual compliance reporting to Squamish Nation","Competency":"Indigenous cultural awareness; SNEAA condition knowledge; Chance-find procedure; Respectful engagement protocols","Training":"Indigenous cultural safety training (mandatory new hire + annual refresher); SNEAA condition awareness briefing; Archaeological chance-find procedure practical; Gender and cultural safety training","Residual":"Low","Reg Ref":"SNEAA; BC Environmental Assessment Act; UNDRIP; Heritage Conservation Act (BC)","LSR":"N/A","SIF":"NO","KPI":"SNEAA condition compliance %; Cultural incident count; Training completion rate"},
    {"Area":"Liquefaction - Cold End","Task":"Flare System Operations & Radiant Heat Management","Role":"Operator","Phase":"Normal Ops / Startup / Emergency","Hazards":"Radiant heat from flare tip (140m stack) igniting adjacent vegetation; Flare flame-out (unburned hydrocarbon release); Flare tip maintenance at height with hot/toxic residues; Flare header back-pressure affecting process safety relief","Consequence":"Forest fire from radiant heat; Toxic/flammable gas release from flame-out; Fall/burn fatality during flare maintenance; Relief device back-pressure failure","Pre-Risk":"High","Controls":"Radiant heat flux monitoring at vegetation boundary; Vegetation management zone (cleared/irrigated buffer); Flare pilot monitoring with auto-relight; Flare tip inspection via drone (minimize WAH); Flare header pressure monitoring; Pre-startup flare capacity verification; Fire suppression capability at vegetation boundary","Competency":"Flare system operations; Radiant heat hazard awareness; Flare header pressure management; Vegetation fire response","Training":"Classroom: Flare system theory + radiant heat; OTS: Flare scenarios during upset/startup; Wildfire response coordination with BC Wildfire Service; Annual refresher","Residual":"Medium","Reg Ref":"CSA Z276; NFPA 59A; BC Wildfire Act; WorkSafeBC","LSR":"LSR-04: Safety Controls","SIF":"YES","KPI":"Flare reliability %; Radiant heat exceedance events; Vegetation inspection compliance %"},
]

all_data.extend(new_entries)

# Update single-train and shift rotation info into startup/shutdown controls
for rec in all_data:
    if "Startup" in rec.get("Phase","") or "Shutdown" in rec.get("Phase",""):
        if "single train" not in rec.get("Controls","").lower():
            rec["Controls"]+=" | SINGLE TRAIN: No redundancy—any failure = full plant outage. 7/7 shift rotation fatigue management critical during extended startup campaigns."
    if "Composite" not in rec.get("Controls","") and "Emergency" in rec.get("Phase",""):
        if "ERT" in rec.get("Controls","") or "rescue" in rec.get("Controls","").lower():
            rec["Controls"]+=" | ERT MODEL: Composite team (2 FT + volunteer operators). Passive firefighting only—no offensive interior attack capability. Helipad + marine ambulance for medevac."

with open(os.path.join(base,"cri_data_v2.json"),"w") as f:
    json.dump(all_data,f,indent=2)
print(f"V2 data complete: {len(all_data)} total CRI entries saved.")
