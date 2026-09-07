# LNG: Safety-Sensitive Positions (SSP) Registry
**Project Phase:** Commissioning, Transition, Operations, Maintenance & Turnarounds  
**Location:** Squamish, British Columbia  
**Governing Regulations:** WorkSafeBC OHS Regulation (Part 3 & Part 23), BC Energy Regulator (BCER) LNG Facility Regulation, Canadian Model for Providing a Safe Workplace  

---

## 1. Definition of a Safety-Sensitive Position (SSP)
In accordance with Canadian safety standards and WorkSafeBC guidelines, a **Safety-Sensitive Position** is defined as any role where impaired performance, cognitive fatigue, or a lapse in decision-making/alertness could result in:
*   A catastrophic process safety event (e.g., Loss of Primary Containment of LNG, BLEVE, or toxic gas release).
*   Direct, fatal, or severe injury to the worker, coworkers, or the public.
*   Catastrophic damage to critical facility infrastructure or the surrounding marine environment (Howe Sound).

---

## 2. Risk ID Nomenclature & Prefix Legend
The Risk IDs mapped under "Critical Barriers Owned" correspond to specific hazard categories in the LNG risk registers:

| Prefix | Hazard Category | Description & Examples | Mapped Register |
| :--- | :--- | :--- | :--- |
| **`CRIT`** | Critical SIMOPS & Commissioning | Bypasses, first gas introduction, SIMOPS ignition sources. | Transition Register |
| **`LOTO`** | Lockout / Tagout | Energy isolations, valve/electrical boundary locks. | Transition Register |
| **`CSE`** | Confined Space Entry | Multi-jurisdictional confined spaces, vessel entries. | Transition Register |
| **`WAT`** | Over-Water Work | Jetty constructions, falls over marine environments. | Transition Register |
| **`UTIL`** | Purging & Utilities | Nitrogen asphyxiation, high-voltage substations. | Transition Register |
| **`CHEM`** | Hazardous Chemicals | Ammonia refrigerant systems, chemical handling. | Transition Register |
| **`MAR`** | Marine Terminal Operations | Loading arm maneuvers, ship-to-shore vessel lines. | Transition Register |
| **`TS`** | Pressure Testing | Hydrostatic/pneumatic line ruptures. | Transition Register |
| **`ENV`** | Environmental Compliance | Underwater noise, flaring limits, emission controls. | Transition Register |
| **`OPS`** | Commissioning & Operations | Thermal shock (banana effect), CUI piping failures. | Transition Register |
| **`REG`** | Regulatory Compliance | Leave to Open (LTO) approvals, BCER conditions. | Transition Register |
| **`LIFT`** | SIMOPS Lifting Operations | Heavy module rigging, crane safety, drops. | Transition Register |
| **`VEH`** | Mobile Equipment & Traffic | Site traffic, pedestrian walkways, backing safety. | Transition Register |
| **`OPS-CRIT`** | Continuous Process Safety | Rollover, BLEVE, RPT, alarm floods, ship collisions. | Operations Register |

---

## 3. Safety-Sensitive Positions (SSP) Registry

| Position Title | Key Phase | Critical Safety Responsibilities | Critical Barriers / Risk IDs Owned | Mandatory Competency & Certifications | Fitness & Medical Requirements |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Control Room Operator (CRO) / DCS Panel Operator** | Commissioning & Operations | Monitors safe operating limits (SOLs); manages alarm rationalization; executes Emergency Shutdown (ESD) protocols; oversees plant status. | **CRIT-03** (Bypasses)<br>**OPS-CRIT-05** (Alarm Flooding)<br>**OPS-CRIT-06** (Hydrates) | • Certified Operator Training Simulator (OTS) program<br>• ISA-18.2 Alarm Management training<br>• Annual ESD simulation certification | • Mandatory pre-employment & post-incident D&A testing<br>• Visual/hearing acuity check<br>• Strict cognitive fatigue limit audits |
| **Operations Director / Shift Charge Engineer** | Transition & Operations | Ultimate shift authority; final approver of critical safety bypasses (T-MOCs) and initial gas introduction; directs emergency shut-ins. | **CRIT-02** (First Gas)<br>**REG-01** (Leave to Open)<br>**OPS-CRIT-07** (Turnarounds) | • P.Eng registration or equivalent technical diploma<br>• ICS 300 (Incident Command System) certification<br>• 10+ years LNG operations experience | • Mandatory pre-employment & post-incident D&A testing<br>• Periodic fitness-for-duty medical clearance |
| **SIMOPS Coordinator** | Commissioning & Transition | Manages physical and temporal boundaries between construction work and live commissioning/startup loops; signs interface permits. | **CRIT-01** (SIMOPS)<br>**LOTO-01** (LOTO transition)<br>**LIFT-01** (Critical Lifts) | • Prime Contractor Coordinator training (WorkSafeBC)<br>• Hazard Identification & Risk Assessment (HIRA)<br>• Advanced Permit-to-Work (PTW) issuer cert | • Mandatory pre-employment & post-incident D&A testing |
| **Permit Issuer / Area Authority** | All Phases | Performs physical gas testing (LEL, O2, toxic gas); validates LOTO isolation points in the field; issues high-risk work permits. | **LOTO-01** (LOTO)<br>**CSE-01** (Confined Space)<br>**UTIL-01** (Nitrogen) | • Certified Gas Tester (CSA Z1002 compliant)<br>• Master Isolation Authority certification<br>• Root Cause Analysis (RCA) basic training | • Pre-employment & post-incident D&A testing<br>• Physical ability to walk process structures |
| **Outside Field Operator (Liquefaction / Storage / Marine)** | Transition & Operations | Executes manual valving, LOTO box locking, line walks, and cryogenic cool-down tracking; monitors physical plant loops. | **OPS-02** (Thermal Shock)<br>**OPS-CRIT-03** (Rollover)<br>**OPS-CRIT-04** (Embrittlement) | • Power Engineering certification (Class 3 or 4)<br>• Site-specific SOP and line-walk validation<br>• Cryogenic safety and hazard handling | • Pre-employment & post-incident D&A testing<br>• SCBA user medical fit test<br>• Confined space rescue capability |
| **Marine Terminal Supervisor / Jetty Operator** | Transition & Operations | Manages LNG carrier berthing, loading arm connection, mooring tension, seawater curtain flows, and Emergency Release Systems (ERS). | **MAR-01** (Loading Arms)<br>**OPS-CRIT-01** (RPT on Water)<br>**OPS-CRIT-08** (Jetty Collision) | • Transport Canada marine terminal certification<br>• ERS/ERC system test and manual override training<br>• Water-activated PFD & rescue boat coxswain cert | • Pre-employment & post-incident D&A testing<br>• Water rescue fitness and swimming check |
| **High-Voltage Electrical Technician** | Commissioning & Maintenance | Performs high-voltage switching, utility energization, substation maintenance, and sets up arc flash boundaries. | **UTIL-02** (Arc Flash / HV)<br>**LOTO-01** (LOTO) | • Red Seal Electrical Journeyman (or equivalent)<br>• CSA Z462 Electrical Safety training<br>• Certified High-Voltage Switching Operator | • Pre-employment & post-incident D&A testing<br>• Color-blindness screening (for wiring diagnostics) |
| **Instrumentation & Control (I&C) Technician** | Commissioning & Maintenance | Calibrates fixed fire & gas (F&G) detectors; tests ESD valves; programs DCS interlocks and safety-instrumented systems (SIS). | **CRIT-03** (Bypasses)<br>**CHEM-01** (Ammonia Leak)<br>**OPS-CRIT-05** (SIS) | • Instrumentation Journeyman certification<br>• TUV Functional Safety Engineer certification (preferred)<br>• Safety Instrumented Systems (SIS) standard training | • Pre-employment & post-incident D&A testing |
| **Emergency Response Team (ERT) Leader** | All Phases | Directs industrial fire, cryogenic vapor cloud dispersion, ammonia leak containment, and marine search and rescue. | **CHEM-01** (Ammonia)<br>**OPS-CRIT-02** (BLEVE)<br>**WAT-01** (Falls Over Water) | • NFPA 1081 (Industrial Fire Brigade Member)<br>• NFPA 472 / 1072 (Hazardous Materials Technican)<br>• Advanced First Aid / First Responder | • Annual high-rigor cardiovascular & physical fit test<br>• Claustrophobia/SCBA entry medical clearance<br>• Pre-employment & post-incident D&A testing |

---

## 4. Fitness-for-Duty & Fatigue Management Protocols (FRMS)
To ensure safety-sensitive positions operate without impairment, LNG enforces the following **Fatigue Risk Management System (FRMS)** and **Fitness-for-Duty** policies:

### 4.1. Shift & Hours of Service Limits
1.  **Maximum Shift Length:** No operator in an SSP may work a shift exceeding 12 hours (excluding exceptional emergency plant shut-ins).
2.  **Minimum Rest Period:** A mandatory minimum of 11 hours of continuous rest must be provided between shifts.
3.  **Maximum Consecutive Shifts:** 
    *   Maximum of 4 consecutive night shifts (12-hour duration).
    *   Maximum of 6 consecutive day shifts (12-hour duration).
    *   A mandatory 3 days rest must follow any night shift rotation.
4.  **Overtime Cap:** Weekly work hours must not exceed 60 hours under any circumstances for SSP roles, and any shift extensions require Operations Manager approval.

### 4.2. Impairment & Drug and Alcohol (D&A) Policy
1.  **Zero-Tolerance Threshold:** All safety-sensitive roles are subject to a zero-tolerance policy for alcohol, recreational cannabis, and illicit substances.
2.  **Testing Triggers:**
    *   **Pre-Employment/Placement:** Mandatory testing before any employee or contractor is placed in an SSP role.
    *   **Reasonable Cause:** Testing triggered by observable slurred speech, balance issues, or erratic behavior.
    *   **Post-Incident/Near-Miss:** Mandatory screening for any operator involved in a process safety event, near-miss, or vehicle collision within 2 hours of the event.
    *   **Random Testing:** Conducted in compliance with Canadian human rights guidelines for highly hazardous environments where safety is critical to site protection.
3.  **Prescription Medications:** Employees in SSP roles are legally required to declare any prescription or over-the-counter medication that contains drowsiness warnings to the Occupational Health Nurse before starting their shift. A temporary non-hazardous duties re-assignment will be arranged if required.

### 4.3. Cognitive Fatigue Monitoring & Self-Assessment
1.  **Shift Start FLHA Integration:** All field and control room operators must complete a brief self-assessment of sleep duration (aiming for >6 hours) and fatigue level as part of their daily Field-Level Hazard Assessment.
2.  **CRO Rotation/Breaks:** Control room operators must stand down and rotate screens every 4 hours to prevent visual habituation and maintain alarm alertness.
3.  **Peer-to-Peer Checkpoints:** Shift Supervisors must conduct active face-to-face field walkdowns and briefings at the 6-hour mark of every 12-hour shift to assess the mental alertness of all personnel in SSP roles.
