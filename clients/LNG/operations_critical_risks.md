# Continuous Operations Critical Safety Risk Register
**Project Phase:** Continuous Operations, Maintenance & Shutdowns (Turnarounds)  
**Primary Location:** British Columbia, Canada (LNG, Squamish)  
**Governing Jurisdictions:** BC Energy Regulator (BCER), WorkSafeBC, Technical Safety BC, CSA Z276, CSA Z1000, CSA Z1002  
*Cross-Jurisdictional Note: Equivalent WorkSafeNB (New Brunswick) OHS Regulation 91-191 clauses are cross-referenced for completeness.*

---

## 1. Overview & Risk Matrix
This risk register identifies and prioritizes hazards associated with the continuous operational phase of the LNG production, storage, and marine export facility. It assumes all commissioning and transition-to-operations activities have been completed and the facility is running under live hydrocarbon conditions.

Risk ratings are determined using a standard 5x5 Likelihood and Severity matrix:
*   **Likelihood (L):** 1 (Rare) to 5 (Almost Certain)
*   **Severity (S):** 1 (Negligible) to 5 (Catastrophic/Fatality)
*   **Risk Level (R):** Likelihood x Severity (Score 1-25)

---

## 2. Risk ID Nomenclature & Prefix Legend
The Risk IDs mapped in this register correspond to specific hazard categories:

| Prefix | Hazard Category | Description & Examples | Mapped Register |
| :--- | :--- | :--- | :--- |
| **`CRIT`** | Critical SIMOPS & Commissioning | Bypasses, initial gas introduction, interface ignition sources. | Transition Register |
| **`LOTO`** | Lockout / Tagout | Energy isolation controls, boundary lockboxes, and handovers. | Transition Register |
| **`CSE`** | Confined Space Entry | Tank/vessel entry, blind lists, atmospheric testing, and sentry logs. | Transition Register |
| **`WAT`** | Over-Water Work | Jetty access, falls over marine environments, and personal flotation. | Transition Register |
| **`UTIL`** | Purging & Utilities | Nitrogen asphyxiation, high-voltage switching, and arc flash. | Transition Register |
| **`CHEM`** | Hazardous Chemicals | Ammonia leak detection, deluge systems, and chemical handling. | Transition Register |
| **`MAR`** | Marine Terminal Operations | Loading arm cryogenic tests, ERS validation, and vessel berthing. | Transition Register |
| **`TS`** | Pressure Testing | Hydrotest boundary lines, transducer calibration, and line rupture. | Transition Register |
| **`ENV`** | Environmental Compliance | Acoustic limits, vessel speeds, flaring limits, MMO logs. | Transition Register |
| **`OPS`** | Commissioning & Ops | Thermal shock cool-down, CUI piping checks, document packages. | Transition Register |
| **`REG`** | Regulatory Approvals | BCER permit conditions, Federal/Provincial Leave to Open. | Transition Register |
| **`LIFT`** | SIMOPS Critical Lifting | Crane lifts, module rigging, and drop zones. | Transition Register |
| **`VEH`** | Mobile Equipment | Traffic management, speed control, pedestrian separation. | Transition Register |
| **`OPS-CRIT`** | Continuous Process Safety | BLEVE vapor clouds, RPT, tank rollover, alarm flooding. | Operations Register |

---

## 3. Operations Critical Risk Register

 | Risk ID | Hazard & Scenario | Pre-Control Risk (L x S = R) | Governing Regulations & Standards | Critical Controls (Preventative & Mitigative) | Critical Control Verification (CCV) Methods | Residual Risk (L x S = R) | 
 | :--- | :--- | :--- | :--- | :--- | :--- | :--- | 
 | **OPS-CRIT-01** | **Rapid Phase Transition (RPT) / Cryogenic Spill on Water**<br>Catastrophic LNG spill onto seawater during loading or marine transit triggers a physical, non-combustible explosion due to rapid boiling, creating a massive overpressure wave and damaging jetty/vessel structures. | **3 (Possible) x 5 (Catastrophic) = 15 (CRITICAL)** | • BC Energy Regulator (BCER) LNG Facility Regulation<br>• CSA Z276 Clause 11 (Operations & Maintenance)<br>• Transport Canada Marine Safety | **Preventative Controls:**<br>1. Implement quick-release Emergency Release Systems (ERS) on loading arms with automatic dry-break couplers.<br>2. Enforce structural containment barriers (drip trays) to prevent LNG from reaching the seawater splash zone.<br><br>**Mitigative Controls:**<br>1. Automated seawater thermal barrier spray systems to warm spilled LNG before it reaches the sea surface.<br>2. Maintain a 100% active exclusion zone around the terminal during transfer operations. | **Verification Method:**<br>Functional loop test of loading arm ERS and check seawater curtain thermal barrier flow (Pre-loading by Terminal Supervisor). | **1 (Rare) x 5 (Catastrophic) = 5 (MEDIUM)** | 
 | **OPS-CRIT-02** | **BLEVE of Refrigerant Storage (Boiling Liquid Expanding Vapor Explosion)**<br>External fire exposure (e.g., pool fire or jet fire) to pressurized mixed refrigerant storage vessels (propane, ethane) leads to vessel shell failure, catastrophic rupture, and a massive fireball. | **3 (Possible) x 5 (Catastrophic) = 15 (CRITICAL)** | • BCER LNG Facility Regulation<br>• CSA Z276 Clause 10 (Fire Protection)<br>• Technical Safety BC | **Preventative Controls:**<br>1. Apply certified passive fireproofing (PFP) insulation to vessel support legs and skirts.<br>2. Maintain double-barrier process control loops on vessel level and pressure systems.<br><br>**Mitigative Controls:**<br>1. Implement automatic High-Volume Water Deluge cooling systems on all refrigerant storage vessels.<br>2. Establish remote-actuated emergency depressurization (blowdown) systems to dump inventory to the flare within 15 minutes of fire detection. | **Verification Method:**<br>Verify passive fireproofing (PFP) thickness coating checks and test automatic vessel deluge loops (Annual by Maintenance Inspector). | **1 (Rare) x 5 (Catastrophic) = 5 (MEDIUM)** | 
 | **OPS-CRIT-03** | **LNG Storage Tank Rollover**<br>Stratification/layering of LNG of different densities and temperatures in storage tanks leads to sudden, rapid mixing (rollover). This causes massive, sudden boil-off, overpressurizing the tank beyond relief valve capacities. | **2 (Unlikely) x 5 (Catastrophic) = 10 (HIGH)** | • CSA Z276 Clause 7 (LNG Storage)<br>• NFPA 59A | **Preventative Controls:**<br>1. Install dual-nozzle filling systems (top and bottom filling) to promote continuous mixing based on cargo density.<br>2. Implement a multi-point density and temperature profiling system (LTMS) at 1-meter intervals throughout the tank height.<br><br>**Mitigative Controls:**<br>1. Configure automatic Boil-Off Gas (BOG) compressor override systems to maximize vapor extraction during pressure spikes.<br>2. Pre-program emergency gas-to-flare routing if tank pressures exceed safe operating limits. | **Verification Method:**<br>Verify DCS tank density/temperature profile tracking and BOG compressor interlocks (Shiftly by Control Room Operator). | **1 (Rare) x 5 (Catastrophic) = 5 (MEDIUM)** | 
 | **OPS-CRIT-04** | **Cryogenic Embrittlement & Structural Collapse**<br>A cryogenic liquid leak (LNG or liquid refrigerant) contacts carbon steel structural supports, causing immediate cold embrittlement and catastrophic collapse of pipe racks, equipment, or vessels. | **3 (Possible) x 5 (Catastrophic) = 15 (CRITICAL)** | • CSA Z276 Clause 5 (Materials)<br>• ASME B31.3 (Process Piping) | **Preventative Controls:**<br>1. Clad critical carbon steel support members with Cryogenic Spill Protection (CSP) epoxy/insulation.<br>2. Install engineered cryogenic deflection shields and drip trays beneath all flanges/valves containing liquid hydrocarbons.<br><br>**Mitigative Controls:**<br>1. Install low-temperature fiber-optic leak detection loops along high-risk piping runs.<br>2. Maintain rapid-isolation ESD valves to limit spill volumes. | **Verification Method:**<br>Perform fiber-optic leak detection loop testing and inspect drip tray integrity (Monthly by Asset Integrity Tech). | **1 (Rare) x 5 (Catastrophic) = 5 (MEDIUM)** | 
 | **OPS-CRIT-05** | **Process Alarm Flooding & Operator Cognitive Overload**<br>During a major process upset, the Distributed Control System (DCS) floods operators with hundreds of alarms in minutes, causing them to miss critical warnings and fail to prevent a catastrophic escalation. | **4 (Likely) x 4 (Major) = 16 (CRITICAL)** | • CSA Z276 Clause 11.2 (Training)<br>• ISA-18.2 (Management of Alarm Systems) | **Preventative Controls:**<br>1. Enforce a strict Alarm Rationalization Program in accordance with ISA-18.2 (targeting <1 alarm per operator per 10 minutes under normal operations).<br>2. Implement dynamic alarm suppression/shelving to silence secondary alarms during major trips.<br><br>**Mitigative Controls:**<br>1. Deploy a High-Performance HMI (Human-Machine Interface) design that visually highlights critical safety parameters.<br>2. Set up automated safety-instrumented shutdown systems (SIS) that act independently of operator intervention. | **Verification Method:**<br>Perform alarm rate auditing and test dynamic alarm suppression logic (Quarterly by Automation Engineer). | **2 (Unlikely) x 4 (Major) = 8 (MEDIUM)** | 
 | **OPS-CRIT-06** | **Hydrate / Ice Plug Formation & Piping Rupture**<br>Moisture ingress into dry feed gas or cryogenic piping loops forms ice or hydrate plugs, causing local blockage, process backpressure, and sudden pipe rupture or projectile generation when warmed or pressurized. | **3 (Possible) x 4 (Major) = 12 (HIGH)** | • CSA Z276 Clause 11.5 (Maintenance)<br>• ASME B31.3 | **Preventative Controls:**<br>1. Maintain continuous moisture analyzer monitoring on the dry gas feed loop, set to trigger an automatic process shutdown if moisture exceeds 0.5 ppm.<br>2. Run regular regeneration cycles on the molecular sieve dehydration beds.<br><br>**Mitigative Controls:**<br>1. Pre-stage chemical injection ports (methanol/glycol) to depress and dissolve hydrate plugs.<br>2. Mandate slow, controlled depressurization procedures for clearing blocked loops. | **Verification Method:**<br>Monitor dehydration loop moisture analyzers in DCS and test methanol injection ports (Daily / Shiftly by CRO). | **1 (Rare) x 4 (Major) = 4 (LOW)** | 
 | **OPS-CRIT-07** | **Turnaround & Shutdown Isolation Failures**<br>During major maintenance turnarounds, contractors perform work under incorrect or bypassed isolations, causing toxic exposure, asphyxiation, or ignition of trapped hydrocarbons. | **4 (Likely) x 5 (Catastrophic) = 20 (CRITICAL)** | • WorkSafeBC OHS Reg Part 10 (LOTO)<br>• NB OHS Reg 91-191 Sec 239-240 | **Preventative Controls:**<br>1. Enforce a digitized, software-tracked Permit to Work (PTW) and LOTO system with mandatory physical validation by Area Authority.<br>2. Mandate double block and bleed (DBB) or physical blinding of all hydrocarbon lines before handing systems over to maintenance.<br><br>**Mitigative Controls:**<br>1. Require independent third-party verification audits on all turnaround isolations.<br>2. Maintain active field safety patrols and gas-testing sweeps in maintenance zones. | **Verification Method:**<br>Conduct turnaround safety audits, double-isolation (DBB) line walkdowns, and verify blind lists (Daily during turnaround by Area Authority). | **1 (Rare) x 5 (Catastrophic) = 5 (MEDIUM)** | 
 | **OPS-CRIT-08** | **Marine Vessel Collision at Jetty**<br>An LNG carrier or escort tug loses propulsion or steering and collides with the marine terminal jetty, causing catastrophic rupture of loading arms and gas release. | **3 (Possible) x 5 (Catastrophic) = 15 (CRITICAL)** | • Transport Canada Marine Safety<br>• Canada Shipping Act<br>• TERMPOL Code requirements | **Preventative Controls:**<br>1. Mandate the use of certified harbor pilots and dedicated escort tugs for all arriving and departing carriers.<br>2. Install active laser docking and jetty-mounted wind/wave monitoring systems.<br><br>**Mitigative Controls:**<br>1. Quick-Release Hooks (QRHs) equipped with remote-release capability and load tension sensors.<br>2. Automatic ESD trigger upon mooring tension limit breach to isolate marine loading headers. | **Verification Method:**<br>Inspect laser docking system calibration records and check Quick-Release Hook tension monitors (Monthly by Marine Engineer). | **1 (Rare) x 5 (Catastrophic) = 5 (MEDIUM)** | 

---

## 4. Life-Saving Rules (LSR) Mapping for Continuous Operations
These operations-phase risks align directly with the **IOGP Life-Saving Rules**:

| Life-Saving Rule | Mapped Operations Risk ID | Operational Application |
| :--- | :--- | :--- |
| **Bypassing Safety Controls** | **OPS-CRIT-05** | Overriding process alarms, disabling safety-instrumented systems (SIS), or ignoring Safe Operating Limits (SOLs). |
| **Confined Space** | **OPS-CRIT-07** | Vessel entry during turnaround maintenance. Requiring active ventilation and oxygen monitoring. |
| **Driving** | *General Operations* | Site logistics and vehicle-pedestrian segregation in loading zones. |
| **Energy Isolation** | **OPS-CRIT-07** | Double block and bleed (DBB) or line blinding requirements before turnaround maintenance begins. |
| **Hot Work** | **OPS-CRIT-07** | Hot work permits during shutdowns near pressurized or unpurged piping. |
| **Line of Fire** | **OPS-CRIT-01**, **OPS-CRIT-04** | Positioning relative to high-pressure loading arms (RPT hazard) and potential cryogenic structural failures. |
| **Safe Mechanical Lifting** | *General Maintenance* | Crane and rigging safety rules during turnaround equipment change-outs. |
| **Work Authorization** | **OPS-CRIT-05**, **OPS-CRIT-07** | Permit to Work compliance. Refusing work if process alarms or safety interlocks are compromised. |
| **Working at Height** | *General Operations* | Accessing high-elevation structures (e.g., storage tank roofs, absorber columns). |

---

## 5. Maintenance & Review Protocol
1. **Frequency:** The continuous operations risk register must be reviewed quarterly by the Operations, Process Safety, and EHS Management team.
2. **Trigger Events:** Any process safety incident (Tier 1 or Tier 2 Loss of Primary Containment), high-potential (HiPo) near-miss, process modification (MOC), or alarm flood event must trigger an immediate review of the affected risk items.
3. **Audit Schedule:** Key mitigative barriers (e.g., ERS loops, water deluge systems, cryogenic epoxy integrity, and alarm flood shelving code) must be physically tested and audited annually.
