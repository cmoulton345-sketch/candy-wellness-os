import os
import json

base_dir = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC"
os.makedirs(base_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. LOAD PREVIOUS MODULES DATA
# -------------------------------------------------------------
with open(os.path.join(base_dir, "build_master_study_suite.py"), "r", encoding="utf-8") as f:
    orig_code = f.read()

# Extract modules_data from previous file
start_idx = orig_code.find("modules_data = [")
end_idx = orig_code.find("\n# -------------------------------------------------------------\n# STEP 1:")
modules_data_str = orig_code[start_idx + len("modules_data = "):end_idx].strip()
modules_data = json.loads(modules_data_str)

# -------------------------------------------------------------
# 2. DEFINE ANATOMICAL ATLAS DATA (WITH LABELED PARTS)
# -------------------------------------------------------------
atlas_data = [
    {
        "id": "cell",
        "title": "1. Human Cell Ultrastructure & Organelles",
        "system": "Cell Biology (Module 2 • Chapter 3)",
        "badge": "Module 2",
        "img": "images/human_cell_labeled.jpg",
        "img_secondary": None,
        "description": "High-magnification cross-section illustrating the internal cellular architecture, metabolic organelles, and protective membrane.",
        "parts": [
            {"name": "Nucleus", "role": "The control center of the cell; houses DNA chromosomes and directs protein synthesis."},
            {"name": "Nucleoli (Nucleolus)", "role": "Dense dark-staining region within the nucleus that synthesizes ribosomal RNA (rRNA)."},
            {"name": "Mitochondria", "role": "The 'powerhouses of the cell'; generates ATP energy via aerobic cellular respiration."},
            {"name": "Ribosomes", "role": "Protein factories composed of rRNA; translate mRNA transcripts into polypeptide chains."},
            {"name": "Rough Endoplasmic Reticulum", "role": "Membranous network studded with ribosomes; folds and modifies nascent proteins."},
            {"name": "Smooth Endoplasmic Reticulum", "role": "Agranular network for lipid and steroid synthesis, calcium storage, and drug detox."},
            {"name": "Golgi Complex (Apparatus)", "role": "Stack of flattened sacs that chemically modifies, sorts, and packages glycoproteins for secretion."},
            {"name": "Lysosomes", "role": "'Digestive bags' packed with hydrolytic acid enzymes to recycle damaged organelles and bacteria."},
            {"name": "Centrioles", "role": "Paired barrel-shaped organelles that organize the mitotic spindle during cell division (mitosis)."},
            {"name": "Plasma Membrane", "role": "Selectively permeable phospholipid bilayer regulating what enters and leaves the cytoplasm."},
            {"name": "Microvilli", "role": "Finger-like membrane folds that increase absorptive surface area (prominent in intestine/kidney)."}
        ]
    },
    {
        "id": "skin",
        "title": "2. Integumentary System Architecture & Receptors",
        "system": "The Skin & Appendages (Module 3 • Chapter 6)",
        "badge": "Module 3",
        "img": "images/skin_layers_receptors_labeled.jpg",
        "img_secondary": "images/skin_3d_cross_section.jpg",
        "description": "3D anatomical block diagram displaying the three principal skin layers, epidermal strata, hair follicle, glands, and cutaneous mechanoreceptors.",
        "parts": [
            {"name": "Epidermis", "role": "Avascular superficial protective layer of stratified squamous keratinized epithelium (5 strata)."},
            {"name": "Stratum Basale", "role": "Deepest epidermal monolayer of stem cells undergoing active mitosis; houses melanocytes."},
            {"name": "Stratum Corneum", "role": "Outermost layer of dead, fully keratinized, shingle-like cells providing waterproof barrier."},
            {"name": "Dermis", "role": "Vascular, tough connective tissue layer (20x thicker than epidermis) containing nerves, vessels, and fibers."},
            {"name": "Papillary Dermis", "role": "Superficial dermal layer with dermal papillae forming fingerprint ridges and housing Meissner corpuscles."},
            {"name": "Reticular Dermis", "role": "Deep dense irregular connective tissue layer rich in collagen and elastin; houses Pacinian corpuscles."},
            {"name": "Hypodermis (Subcutaneous)", "role": "Adipose tissue foundation providing thermal insulation, energy reserve, and shock cushioning."},
            {"name": "Meissner Corpuscle", "role": "Encapsulated tactile receptor in dermal papillae that detects light touch and low-frequency vibration."},
            {"name": "Pacinian Corpuscle", "role": "Large lamellated onion-shaped receptor deep in reticular dermis/hypodermis detecting deep pressure."},
            {"name": "Free Nerve Endings", "role": "Unencapsulated sensory dendrites extending into epidermis to detect nociceptive pain and temperature."},
            {"name": "Sebaceous Glands", "role": "Oil glands attached to hair follicles secreting sebum to lubricate hair/skin and prevent microbial growth."},
            {"name": "Eccrine Sweat Glands", "role": "Coiled tubular glands distributed across the body that secrete watery sweat for thermoregulation."},
            {"name": "Arrector Pili Muscle", "role": "Smooth muscle bundle contracting under sympathetic stimulation to pull hair upright ('goosebumps')."}
        ]
    },
    {
        "id": "skeleton",
        "title": "3. The Complete Human Skeleton (Axial & Appendicular)",
        "system": "Skeletal System (Module 4 • Chapter 7)",
        "badge": "Module 4",
        "img": "images/skeleton_complete_labeled.jpg",
        "img_secondary": None,
        "description": "Anterior and posterior full-body skeletal views illustrating all 206 bones, categorized into the 80 axial bones and 126 appendicular bones.",
        "parts": [
            {"name": "Cranium & Facial Bones", "role": "Axial: Protects brain (Frontal, Parietal, Occipital) and frames face (Maxilla, Zygomatic, Mandible)."},
            {"name": "Vertebral Column", "role": "Axial: Flexible supportive column with 7 Cervical, 12 Thoracic, 5 Lumbar, Sacrum, and Coccyx."},
            {"name": "Thoracic Cage", "role": "Axial: Bony protection for heart/lungs composed of Sternum and 12 pairs of ribs (7 True, 3 False, 2 Floating)."},
            {"name": "Pectoral Girdle", "role": "Appendicular: Attaches upper limbs to axial trunk; includes Clavicle (collarbone) and Scapula (shoulder blade)."},
            {"name": "Humerus", "role": "Appendicular: Long bone of the upper arm articulating with glenoid cavity and elbow."},
            {"name": "Radius & Ulna", "role": "Appendicular: Forearm bones; Radius is lateral (thumb side) and Ulna is medial (pinky side)."},
            {"name": "Carpals, Metacarpals, Phalanges", "role": "Appendicular: Wrist (8 carpals), palm (5 metacarpals), and fingers (14 phalanges)."},
            {"name": "Pelvic Girdle (Coxal Bone)", "role": "Appendicular: Sturdy weight-bearing ring formed by fused Ilium, Ischium, and Pubis bones."},
            {"name": "Femur", "role": "Appendicular: Heaviest, strongest, and longest bone in the body; articulates with acetabulum at hip."},
            {"name": "Patella", "role": "Appendicular: Sesamoid kneecap protecting the knee joint and improving quadriceps leverage."},
            {"name": "Tibia & Fibula", "role": "Appendicular: Lower leg; Tibia (shinbone) is medial and weight-bearing; Fibula is lateral stabilizer."},
            {"name": "Tarsals, Metatarsals, Calcaneus", "role": "Appendicular: Ankle (7 tarsals), heel (calcaneus), arch (5 metatarsals), and toes (14 phalanges)."}
        ]
    },
    {
        "id": "muscles",
        "title": "4. Major Superficial Skeletal Muscles (Anterior & Posterior)",
        "system": "Muscular System (Module 5 • Chapter 8)",
        "badge": "Module 5",
        "img": "images/muscles_anterior_labeled.jpg",
        "img_secondary": "images/muscles_posterior_labeled.jpg",
        "description": "Full-length anatomical plates detailing superficial muscle groups, prime movers, antagonists, and joint movements from both anterior and posterior perspectives.",
        "parts": [
            {"name": "Sternocleidomastoid", "role": "Neck muscle that flexes neck and rotates head to opposite side."},
            {"name": "Trapezius", "role": "Large triangular upper back/neck muscle that elevates, depresses, and retracts the scapula."},
            {"name": "Deltoid", "role": "Triangular shoulder muscle that serves as the prime mover of arm abduction."},
            {"name": "Pectoralis Major", "role": "Large chest muscle that adducts, flexes, and medially rotates the humerus at the shoulder."},
            {"name": "Biceps Brachii", "role": "Anterior arm muscle that is the prime mover of elbow flexion and powerful forearm supinator."},
            {"name": "Triceps Brachii", "role": "Posterior arm muscle that acts as the primary antagonist to biceps, extending the elbow joint."},
            {"name": "Rectus Abdominis", "role": "'Six-pack' abdominal muscle that flexes the lumbar vertebral column and compresses abdominal cavity."},
            {"name": "External Obliques", "role": "Lateral abdominal muscles that rotate and laterally flex the trunk."},
            {"name": "Latissimus Dorsi", "role": "'Swimmer's muscle'; broad lower back muscle that extends and adducts the arm."},
            {"name": "Gluteus Maximus", "role": "Largest muscle in the body; prime mover of hip extension (rising from sitting, climbing stairs)."},
            {"name": "Quadriceps Femoris Group", "role": "Anterior thigh muscles (Rectus femoris, Vastus lateralis, medialis, intermedius) extending the knee."},
            {"name": "Hamstrings Group", "role": "Posterior thigh muscles (Biceps femoris, Semitendinosus, Semimembranosus) flexing knee and extending hip."},
            {"name": "Tibialis Anterior", "role": "Anterior shin muscle that performs ankle dorsiflexion and foot inversion."},
            {"name": "Gastrocnemius & Soleus", "role": "Posterior calf muscles that plantarflex the ankle via the strong Calcaneal (Achilles) tendon."}
        ]
    },
    {
        "id": "endocrine",
        "title": "5. The Human Endocrine System (Master Glands & Hormones)",
        "system": "Endocrine System (Module 8 • Chapter 11)",
        "badge": "Module 8",
        "img": "images/endocrine_system_labeled.jpg",
        "img_secondary": None,
        "description": "Full-body anatomical diagram displaying the exact positions of all master ductless endocrine glands and their secreted chemical messengers.",
        "parts": [
            {"name": "Pineal Gland", "role": "Located in brain epithalamus; secretes Melatonin in darkness to coordinate circadian sleep-wake cycles."},
            {"name": "Hypothalamus", "role": "Master neuroendocrine coordinator; synthesizes ADH and Oxytocin; controls anterior pituitary via releasing hormones."},
            {"name": "Pituitary Gland (Master Gland)", "role": "Anterior lobe secretes TSH, ACTH, GH, PRL, FSH, LH; Posterior lobe stores and releases ADH & Oxytocin."},
            {"name": "Thyroid Gland", "role": "Butterfly-shaped neck gland; secretes T3 & T4 (metabolic rate) and Calcitonin (lowers blood calcium)."},
            {"name": "Parathyroid Glands", "role": "Four tiny glands on posterior thyroid; secrete Parathyroid Hormone (PTH) to elevate blood calcium levels."},
            {"name": "Thymus Gland", "role": "Located behind sternum; secretes Thymosin to program and mature immunocompetent T-lymphocytes."},
            {"name": "Adrenal Glands (Suprarenal)", "role": "Cortex secretes Aldosterone (Na+ retention) and Cortisol (glucose/stress); Medulla secretes Epinephrine."},
            {"name": "Pancreas (Islets of Langerhans)", "role": "Beta cells secrete Insulin (lowers blood glucose); Alpha cells secrete Glucagon (elevates blood glucose)."},
            {"name": "Ovaries (Female)", "role": "Secrete Estrogen (secondary sex characteristics) and Progesterone (menstrual cycle & pregnancy support)."},
            {"name": "Testes (Male)", "role": "Secrete Testosterone (spermatogenesis, muscle mass, secondary male sex characteristics)."}
        ]
    }
]

# -------------------------------------------------------------
# 3. BUILD INTERACTIVE HTML MASTER STUDY HUB WITH ATLAS
# -------------------------------------------------------------
html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rayne's Master A&P Exam Hub (Modules 1–8) — NBCC Practical Nursing</title>
  <style>
    :root {
      --primary: #9d174d;
      --primary-dark: #831843;
      --secondary: #be185d;
      --accent: #f43f5e;
      --bg: #fdf2f8;
      --card-bg: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
      --border: #fbcfe8;
      --success: #16a34a;
      --success-bg: #f0fdf4;
      --danger: #dc2626;
      --danger-bg: #fef2f2;
      --cyan: #0284c7;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 16px;
    }

    .container {
      max-width: 1120px;
      margin: 0 auto;
    }

    header {
      background: linear-gradient(135deg, var(--primary-dark), #4c0519);
      color: white;
      padding: 28px 24px;
      border-radius: 14px;
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(157, 23, 77, 0.25);
      text-align: center;
    }

    header h1 {
      font-size: 2.1rem;
      font-weight: 800;
      margin-bottom: 6px;
      letter-spacing: -0.5px;
    }

    header p {
      opacity: 0.95;
      font-size: 1.05rem;
    }

    .badge-bar {
      margin-top: 12px;
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .badge {
      background: rgba(255, 255, 255, 0.18);
      border: 1px solid rgba(255, 255, 255, 0.35);
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
    }

    /* Mode Navigation Tabs */
    .mode-nav {
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    .mode-btn {
      background: white;
      border: 2px solid var(--primary);
      color: var(--primary);
      padding: 10px 18px;
      border-radius: 30px;
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.25s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .mode-btn.active, .mode-btn:hover {
      background: var(--primary);
      color: white;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(157, 23, 77, 0.3);
    }

    /* Module Filter Strip */
    .module-filter {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 10px;
      margin-bottom: 20px;
    }

    .mod-filter-btn {
      background: white;
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }

    .mod-filter-btn.active {
      background: var(--secondary);
      color: white;
      border-color: var(--secondary);
    }

    /* Section Containers */
    .view-section {
      display: none;
      background: white;
      padding: 26px;
      border-radius: 14px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
      border: 1px solid rgba(251, 207, 232, 0.6);
    }

    .view-section.active {
      display: block;
      animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Quiz Cards */
    .q-card {
      background: #ffffff;
      border: 1px solid #f1f5f9;
      border-left: 4px solid var(--primary);
      border-radius: 10px;
      padding: 18px;
      margin-bottom: 18px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .q-meta {
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--secondary);
      margin-bottom: 8px;
      text-transform: uppercase;
    }

    .q-stem {
      font-size: 1.05rem;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 14px;
    }

    .opt-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .opt-label {
      display: flex;
      align-items: center;
      padding: 10px 14px;
      background: #fdf2f8;
      border: 1.5px solid #fbcfe8;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.95rem;
      font-weight: 500;
      transition: background 0.2s, border 0.2s;
    }

    .opt-label:hover {
      background: #fce7f3;
      border-color: var(--secondary);
    }

    .opt-label input {
      margin-right: 12px;
      accent-color: var(--primary);
      transform: scale(1.15);
    }

    .q-feedback {
      display: none;
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: 8px;
      font-size: 0.92rem;
      line-height: 1.5;
    }

    .q-feedback.correct {
      display: block;
      background: var(--success-bg);
      border-left: 4px solid var(--success);
      color: #14532d;
    }

    .q-feedback.incorrect {
      display: block;
      background: var(--danger-bg);
      border-left: 4px solid var(--danger);
      color: #7f1d1d;
    }

    .quiz-action-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 0;
      border-top: 2px solid var(--border);
      margin-top: 24px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .action-btn {
      background: var(--primary);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      transition: opacity 0.2s;
    }

    .action-btn:hover { opacity: 0.9; }

    .score-box {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--primary);
    }

    /* True/False Blitz */
    .tf-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 18px;
      margin-bottom: 16px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .tf-btn-row {
      display: flex;
      gap: 10px;
      margin-top: 12px;
    }

    .tf-btn {
      flex: 1;
      padding: 10px;
      border: 2px solid #cbd5e1;
      background: #f8fafc;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.2s;
    }

    .tf-btn:hover {
      background: #e2e8f0;
    }

    .tf-btn.selected-true {
      background: var(--success-bg);
      border-color: var(--success);
      color: #166534;
    }

    .tf-btn.selected-false {
      background: var(--danger-bg);
      border-color: var(--danger);
      color: #991b1b;
    }

    /* Flashcard Deck */
    .flashcard-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      max-width: 680px;
      margin: 0 auto;
    }

    .flashcard {
      width: 100%;
      height: 330px;
      perspective: 1000px;
      cursor: pointer;
      margin-bottom: 20px;
    }

    .flashcard-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
      transform-style: preserve-3d;
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    .flashcard.flipped .flashcard-inner {
      transform: rotateY(180deg);
    }

    .fc-face {
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      border-radius: 16px;
      padding: 32px 24px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border: 2px solid var(--border);
    }

    .fc-front {
      background: white;
      color: var(--primary);
    }

    .fc-back {
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      color: white;
      transform: rotateY(180deg);
    }

    .fc-prompt {
      font-size: 1.25rem;
      font-weight: 700;
      line-height: 1.4;
    }

    .fc-meta {
      position: absolute;
      top: 14px;
      left: 20px;
      font-size: 0.85rem;
      font-weight: 700;
      opacity: 0.7;
    }

    .fc-mod {
      position: absolute;
      top: 14px;
      right: 20px;
      background: var(--bg);
      color: var(--primary);
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 0.8rem;
      font-weight: 700;
    }

    .fc-back .fc-mod {
      background: rgba(255, 255, 255, 0.2);
      color: white;
    }

    .fc-nav {
      display: flex;
      gap: 12px;
    }

    /* Blueprints & Atlas */
    .blueprint-grid, .atlas-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 26px;
    }

    .blueprint-item, .atlas-card {
      background: #0f172a;
      color: #e2e8f0;
      border-radius: 12px;
      overflow: hidden;
      border: 2px solid #334155;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }

    .bp-header, .atlas-header {
      padding: 14px 20px;
      background: #1e293b;
      border-bottom: 2px solid #38bdf8;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .bp-title, .atlas-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: #38bdf8;
    }

    .bp-tag, .atlas-badge {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 700;
      border: 1px solid #38bdf8;
    }

    .bp-img-box, .atlas-img-box {
      background: #ffffff;
      padding: 16px;
      text-align: center;
    }

    .bp-img-box img, .atlas-img-box img {
      max-width: 100%;
      height: auto;
      border-radius: 6px;
      display: block;
      margin: 0 auto;
      box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    }

    .bp-summary, .atlas-body {
      padding: 18px 22px;
      font-size: 0.94rem;
      line-height: 1.55;
      background: #0f172a;
    }

    /* Parts Breakdown Table */
    .parts-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 14px;
      background: #1e293b;
      border-radius: 8px;
      overflow: hidden;
    }

    .parts-table th, .parts-table td {
      padding: 10px 14px;
      border-bottom: 1px solid #334155;
      font-size: 0.9rem;
      text-align: left;
    }

    .parts-table th {
      background: #0d1e38;
      color: #38bdf8;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.82rem;
      letter-spacing: 0.5px;
    }

    .parts-table tr:last-child td {
      border-bottom: none;
    }

    .part-name {
      color: #67e8f9;
      font-weight: 700;
      white-space: nowrap;
      width: 25%;
    }

    .part-role {
      color: #cbd5e1;
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <h1>Rayne's Master A&P Study Hub (Modules 1–8)</h1>
      <p>NBCC Practical Nursing (HSCC 1087A) • Instructor: Jessica Freeze Snyder • Exam: Oct 13, 2026</p>
      <div class="badge-bar">
        <span class="badge">📘 Structure & Function 17th Ed</span>
        <span class="badge">🎯 75% Passing Standard</span>
        <span class="badge">🩺 80 MCQs + 40 True/False</span>
        <span class="badge">🔬 Full Labeled Anatomical Atlas</span>
        <span class="badge">🖼️ 8 Concept Blueprints</span>
      </div>
    </header>

    <!-- Top Mode Navigation -->
    <div class="mode-nav">
      <button class="mode-btn active" onclick="switchView('exam')">📝 Practice Exam</button>
      <button class="mode-btn" onclick="switchView('tf')">⚡ True / False Blitz</button>
      <button class="mode-btn" onclick="switchView('flashcards')">🃏 Flashcards Deck</button>
      <button class="mode-btn" onclick="switchView('atlas')">🔬 Anatomical Picture Atlas</button>
      <button class="mode-btn" onclick="switchView('blueprints')">🖼️ Concept Blueprints</button>
    </div>

    <!-- Module Filter Buttons -->
    <div class="module-filter">
      <button class="mod-filter-btn active" onclick="filterModule('all')">All 8 Modules (Full Exam)</button>
      <button class="mod-filter-btn" onclick="filterModule(1)">Mod 1: Intro & Homeostasis</button>
      <button class="mod-filter-btn" onclick="filterModule(2)">Mod 2: Cells & Transport</button>
      <button class="mod-filter-btn" onclick="filterModule(3)">Mod 3: Integumentary & Burns</button>
      <button class="mod-filter-btn" onclick="filterModule(4)">Mod 4: Skeletal & Joints</button>
      <button class="mod-filter-btn" onclick="filterModule(5)">Mod 5: Muscular & Sarcomere</button>
      <button class="mod-filter-btn" onclick="filterModule(6)">Mod 6: Nervous & Reflexes</button>
      <button class="mod-filter-btn" onclick="filterModule(7)">Mod 7: Special Senses</button>
      <button class="mod-filter-btn" onclick="filterModule(8)">Mod 8: Endocrine System</button>
    </div>

    <!-- VIEW 1: PRACTICE EXAM -->
    <section id="exam-view" class="view-section active">
      <div id="quiz-container"></div>
      <div class="quiz-action-bar">
        <button class="action-btn" onclick="submitExam()">Submit Exam & Calculate Score</button>
        <button class="action-btn" style="background:#64748b;" onclick="resetExam()">Reset Choices</button>
        <div id="score-display" class="score-box"></div>
      </div>
    </section>

    <!-- VIEW 2: TRUE / FALSE BLITZ -->
    <section id="tf-view" class="view-section">
      <div id="tf-container"></div>
    </section>

    <!-- VIEW 3: FLASHCARDS -->
    <section id="fc-view" class="view-section">
      <div class="flashcard-wrap">
        <div class="flashcard" id="fc-card" onclick="flipFlashcard()">
          <div class="flashcard-inner">
            <div class="fc-face fc-front">
              <span class="fc-meta" id="fc-idx">Card 1 / 40</span>
              <span class="fc-mod" id="fc-mod-tag">Module 1</span>
              <div class="fc-prompt" id="fc-front-text">Loading question...</div>
            </div>
            <div class="fc-face fc-back">
              <span class="fc-meta">Answer & Concept</span>
              <span class="fc-mod" id="fc-mod-back-tag">Module 1</span>
              <div class="fc-prompt" id="fc-back-text">Loading explanation...</div>
            </div>
          </div>
        </div>
        <div class="fc-nav">
          <button class="action-btn" onclick="prevFlashcard()">← Previous</button>
          <button class="action-btn" style="background:var(--secondary);" onclick="shuffleFlashcards()">🔀 Shuffle</button>
          <button class="action-btn" onclick="nextFlashcard()">Next →</button>
        </div>
      </div>
    </section>

    <!-- VIEW 4: ANATOMICAL PICTURE ATLAS (NEW) -->
    <section id="atlas-view" class="view-section">
      <h2 style="color:var(--primary); margin-bottom:12px; font-size:1.4rem;">🔬 Anatomical Picture Atlas (Full Labeled Figures)</h2>
      <p style="color:var(--text-muted); margin-bottom:20px; font-size:0.95rem;">
        Official high-resolution anatomical illustrations of the <strong>Human Cell, Skin Layers, Skeletal System, Muscular System, and Endocrine Glands</strong> with callout labels and learning keys for Rayne's exam review.
      </p>
      <div class="atlas-grid" id="atlas-container"></div>
    </section>

    <!-- VIEW 5: CONCEPT BLUEPRINTS -->
    <section id="bp-view" class="view-section">
      <h2 style="color:var(--primary); margin-bottom:12px; font-size:1.4rem;">🖼️ High-Yield Concept Blueprints (Summary Quadrants)</h2>
      <p style="color:var(--text-muted); margin-bottom:20px; font-size:0.95rem;">
        Four-quadrant quick reference blueprints for Modules 1 through 8 with zero margin overflow.
      </p>
      <div class="blueprint-grid" id="bp-container"></div>
    </section>

  </div>

  <script>
    const modulesData = """ + json.dumps(modules_data) + """;
    const atlasData = """ + json.dumps(atlas_data) + """;

    let currentModuleFilter = 'all';
    let currentFlashcardIndex = 0;
    let activeFlashcards = [];

    window.onload = function() {
      renderQuiz();
      renderTF();
      initFlashcards();
      renderAtlas();
      renderBlueprints();
    };

    function switchView(viewName) {
      document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));

      if (viewName === 'exam') {
        document.querySelector('.mode-btn:nth-child(1)').classList.add('active');
        document.getElementById('exam-view').classList.add('active');
      } else if (viewName === 'tf') {
        document.querySelector('.mode-btn:nth-child(2)').classList.add('active');
        document.getElementById('tf-view').classList.add('active');
      } else if (viewName === 'flashcards') {
        document.querySelector('.mode-btn:nth-child(3)').classList.add('active');
        document.getElementById('fc-view').classList.add('active');
      } else if (viewName === 'atlas') {
        document.querySelector('.mode-btn:nth-child(4)').classList.add('active');
        document.getElementById('atlas-view').classList.add('active');
      } else if (viewName === 'blueprints') {
        document.querySelector('.mode-btn:nth-child(5)').classList.add('active');
        document.getElementById('bp-view').classList.add('active');
      }
    }

    function filterModule(modId) {
      currentModuleFilter = modId;
      document.querySelectorAll('.mod-filter-btn').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
      renderQuiz();
      renderTF();
      initFlashcards();
      renderAtlas();
      renderBlueprints();
    }

    // 1. RENDER QUIZ
    function renderQuiz() {
      const container = document.getElementById('quiz-container');
      container.innerHTML = '';
      let qCount = 0;

      modulesData.forEach(mod => {
        if (currentModuleFilter !== 'all' && mod.mod_num !== parseInt(currentModuleFilter)) return;

        mod.mcqs.forEach((mcq, idx) => {
          qCount++;
          const qDiv = document.createElement('div');
          qDiv.className = 'q-card';
          qDiv.dataset.ans = mcq.ans;
          qDiv.id = `q-${mod.mod_num}-${idx}`;

          let optsHtml = '';
          mcq.options.forEach(opt => {
            const letter = opt.trim().charAt(0);
            optsHtml += `
              <label class="opt-label">
                <input type="radio" name="opt-${mod.mod_num}-${idx}" value="${letter}">
                ${opt}
              </label>
            `;
          });

          qDiv.innerHTML = `
            <div class="q-meta">
              <span>Question ${qCount} • Module ${mod.mod_num}</span>
              <span>${mod.chapter}</span>
            </div>
            <div class="q-stem">${mcq.q}</div>
            <div class="opt-list">${optsHtml}</div>
            <div class="q-feedback" id="fb-${mod.mod_num}-${idx}">
              <strong>Correct Answer: ${mcq.ans}</strong><br>
              ${mcq.rationale}
            </div>
          `;
          container.appendChild(qDiv);
        });
      });
      document.getElementById('score-display').innerText = '';
    }

    function submitExam() {
      let total = 0;
      let correct = 0;

      document.querySelectorAll('.q-card').forEach(qCard => {
        total++;
        const correctAns = qCard.dataset.ans;
        const selected = qCard.querySelector('input[type="radio"]:checked');
        const feedback = qCard.querySelector('.q-feedback');

        if (selected) {
          if (selected.value === correctAns) {
            correct++;
            feedback.className = 'q-feedback correct';
            feedback.innerHTML = `✅ <strong>Correct! (${correctAns})</strong><br>` + feedback.innerHTML.split('<br>')[1];
          } else {
            feedback.className = 'q-feedback incorrect';
            feedback.innerHTML = `❌ <strong>Incorrect. You selected (${selected.value}). Correct answer is (${correctAns}):</strong><br>` + feedback.innerHTML.split('<br>')[1];
          }
        } else {
          feedback.className = 'q-feedback incorrect';
          feedback.innerHTML = `⚠️ <strong>Unanswered. Correct answer is (${correctAns}):</strong><br>` + feedback.innerHTML.split('<br>')[1];
        }
      });

      const pct = Math.round((correct / total) * 100);
      const scoreBanner = document.getElementById('score-display');
      const passText = pct >= 75 ? '🎉 PASSED (Meets NBCC 75% Standard!)' : '⚠️ Keep Studying (Below 75% NBCC Standard)';
      scoreBanner.innerHTML = `Score: ${correct} / ${total} (${pct}%) — ${passText}`;
      scoreBanner.scrollIntoView({ behavior: 'smooth' });
    }

    function resetExam() {
      document.querySelectorAll('.q-card input[type="radio"]').forEach(r => r.checked = false);
      document.querySelectorAll('.q-feedback').forEach(fb => {
        fb.className = 'q-feedback';
        fb.style.display = 'none';
      });
      document.getElementById('score-display').innerText = '';
    }

    // 2. RENDER TRUE / FALSE
    function renderTF() {
      const container = document.getElementById('tf-container');
      container.innerHTML = '';
      let tfCount = 0;

      modulesData.forEach(mod => {
        if (currentModuleFilter !== 'all' && mod.mod_num !== parseInt(currentModuleFilter)) return;

        mod.true_false.forEach((tf, idx) => {
          tfCount++;
          const card = document.createElement('div');
          card.className = 'tf-card';
          card.innerHTML = `
            <div class="q-meta">
              <span>T/F Question ${tfCount} • Module ${mod.mod_num}</span>
              <span>${mod.chapter}</span>
            </div>
            <div class="q-stem">"${tf.q}"</div>
            <div class="tf-btn-row">
              <button class="tf-btn" onclick="checkTF(this, true, ${tf.ans === 'True'}, '${escapeQuotes(tf.explanation)}')">True</button>
              <button class="tf-btn" onclick="checkTF(this, false, ${tf.ans === 'False'}, '${escapeQuotes(tf.explanation)}')">False</button>
            </div>
            <div class="q-feedback" style="margin-top:12px;"></div>
          `;
          container.appendChild(card);
        });
      });
    }

    function escapeQuotes(str) {
      return str.replace(/'/g, "\\\\'");
    }

    function checkTF(btn, userChoice, isCorrect, explanation) {
      const parent = btn.closest('.tf-card');
      const buttons = parent.querySelectorAll('.tf-btn');
      const fb = parent.querySelector('.q-feedback');

      buttons.forEach(b => {
        b.classList.remove('selected-true', 'selected-false');
      });

      if (userChoice) {
        btn.classList.add('selected-true');
      } else {
        btn.classList.add('selected-false');
      }

      if (isCorrect) {
        fb.className = 'q-feedback correct';
        fb.innerHTML = `✅ <strong>Correct!</strong><br>${explanation}`;
      } else {
        fb.className = 'q-feedback incorrect';
        fb.innerHTML = `❌ <strong>Incorrect!</strong><br>${explanation}`;
      }
      fb.style.display = 'block';
    }

    // 3. FLASHCARDS
    function initFlashcards() {
      activeFlashcards = [];
      modulesData.forEach(mod => {
        if (currentModuleFilter !== 'all' && mod.mod_num !== parseInt(currentModuleFilter)) return;

        mod.mcqs.forEach(mcq => {
          activeFlashcards.push({
            mod: `Module ${mod.mod_num}`,
            front: mcq.q,
            back: `<strong>Answer: ${mcq.ans}</strong><br><br>${mcq.rationale}`
          });
        });
        mod.true_false.forEach(tf => {
          activeFlashcards.push({
            mod: `Module ${mod.mod_num} (T/F)`,
            front: `Statement: "${tf.q}"`,
            back: `<strong>${tf.ans.toUpperCase()}</strong><br><br>${tf.explanation}`
          });
        });
      });

      currentFlashcardIndex = 0;
      updateFlashcardView();
    }

    function updateFlashcardView() {
      if (activeFlashcards.length === 0) return;
      const card = document.getElementById('fc-card');
      card.classList.remove('flipped');

      const cur = activeFlashcards[currentFlashcardIndex];
      document.getElementById('fc-idx').innerText = `Card ${currentFlashcardIndex + 1} / ${activeFlashcards.length}`;
      document.getElementById('fc-mod-tag').innerText = cur.mod;
      document.getElementById('fc-mod-back-tag').innerText = cur.mod;
      document.getElementById('fc-front-text').innerHTML = cur.front;
      document.getElementById('fc-back-text').innerHTML = cur.back;
    }

    function flipFlashcard() {
      document.getElementById('fc-card').classList.toggle('flipped');
    }

    function nextFlashcard() {
      if (currentFlashcardIndex < activeFlashcards.length - 1) {
        currentFlashcardIndex++;
        updateFlashcardView();
      }
    }

    function prevFlashcard() {
      if (currentFlashcardIndex > 0) {
        currentFlashcardIndex--;
        updateFlashcardView();
      }
    }

    function shuffleFlashcards() {
      for (let i = activeFlashcards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [activeFlashcards[i], activeFlashcards[j]] = [activeFlashcards[j], activeFlashcards[i]];
      }
      currentFlashcardIndex = 0;
      updateFlashcardView();
    }

    // 4. RENDER ANATOMICAL PICTURE ATLAS
    function renderAtlas() {
      const container = document.getElementById('atlas-container');
      container.innerHTML = '';

      atlasData.forEach(item => {
        const card = document.createElement('div');
        card.className = 'atlas-card';

        let rows = '';
        item.parts.forEach(p => {
          rows += `
            <tr>
              <td class="part-name">${p.name}</td>
              <td class="part-role">${p.role}</td>
            </tr>
          `;
        });

        let secondaryImgHtml = '';
        if (item.img_secondary) {
          secondaryImgHtml = `
            <div style="margin-top:14px;">
              <img src="${item.img_secondary}?t=3" alt="${item.title} Secondary View" style="max-width:100%; height:auto; border-radius:6px; display:block; margin:0 auto; box-shadow:0 4px 14px rgba(0,0,0,0.08);">
            </div>
          `;
        }

        card.innerHTML = `
          <div class="atlas-header">
            <span class="atlas-title">${item.title}</span>
            <span class="atlas-badge">${item.system}</span>
          </div>
          <div class="atlas-img-box">
            <img src="${item.img}?t=3" alt="${item.title}">
            ${secondaryImgHtml}
          </div>
          <div class="atlas-body">
            <p><strong>Description:</strong> ${item.description}</p>
            <h4 style="color:#38bdf8; margin-top:14px; margin-bottom:6px; font-size:1rem;">📌 Key Labeled Structures & Functions to Memorize:</h4>
            <table class="parts-table">
              <thead>
                <tr>
                  <th>Anatomical Structure</th>
                  <th>Function & Exam Key</th>
                </tr>
              </thead>
              <tbody>
                ${rows}
              </tbody>
            </table>
          </div>
        `;
        container.appendChild(card);
      });
    }

    // 5. RENDER CONCEPT BLUEPRINTS
    function renderBlueprints() {
      const container = document.getElementById('bp-container');
      container.innerHTML = '';

      modulesData.forEach(mod => {
        if (currentModuleFilter !== 'all' && mod.mod_num !== parseInt(currentModuleFilter)) return;

        const bpItem = document.createElement('div');
        bpItem.className = 'blueprint-item';
        bpItem.innerHTML = `
          <div class="bp-header">
            <span class="bp-title">${mod.title}</span>
            <span class="bp-tag">${mod.chapter}</span>
          </div>
          <div class="bp-img-box">
            <img src="${mod.diagram}?t=3" alt="${mod.title}">
          </div>
          <div class="bp-summary">
            <strong>Key Focus Points:</strong> ${mod.summary}
          </div>
        `;
        container.appendChild(bpItem);
      });
    }
  </script>
</body>
</html>
"""

with open(os.path.join(base_dir, "Rayne_AP_Master_Study_Hub_Modules_1_8.html"), "w", encoding="utf-8") as f:
    f.write(html_code)

print("Updated Rayne_AP_Master_Study_Hub_Modules_1_8.html with Anatomical Atlas!")

# -------------------------------------------------------------
# 4. BUILD EXPANDED PRINTABLE BLUEPRINTS & ATLAS (HTML)
# -------------------------------------------------------------
printable_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Rayne's Printable Anatomical Atlas & Blueprints Pack (Modules 1–8)</title>
  <style>
    @page {
      size: letter portrait;
      margin: 0.35in;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Segoe UI', -apple-system, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      padding: 20px;
      line-height: 1.5;
    }

    .no-print-bar {
      background: #1e293b;
      border: 2px solid #38bdf8;
      color: #ffffff;
      padding: 16px 24px;
      border-radius: 10px;
      margin-bottom: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .print-btn {
      background: #38bdf8;
      color: #0f172a;
      border: none;
      padding: 10px 22px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 1rem;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
    }

    .print-btn:hover { background: #7dd3fc; }

    .bp-page {
      background: #1e293b;
      border: 2px solid #38bdf8;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 36px;
      page-break-after: always;
    }

    .bp-title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #38bdf8;
      padding-bottom: 8px;
      margin-bottom: 14px;
    }

    .bp-title {
      font-size: 1.45rem;
      font-weight: 800;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .bp-badge {
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid #38bdf8;
      color: #38bdf8;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 700;
    }

    .bp-diagram-box {
      background: white;
      padding: 10px;
      border-radius: 8px;
      margin-bottom: 14px;
      text-align: center;
    }

    .bp-diagram-box img {
      max-width: 100%;
      max-height: 480px;
      height: auto;
      border-radius: 4px;
      display: block;
      margin: 0 auto;
    }

    .parts-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 10px;
    }

    .part-pill {
      background: #0f172a;
      border-left: 3px solid #38bdf8;
      padding: 8px 12px;
      border-radius: 4px;
      font-size: 0.84rem;
    }

    .part-pill strong {
      color: #67e8f9;
      display: block;
      margin-bottom: 2px;
    }

    @media print {
      body { background: white; color: black; padding: 0; }
      .no-print-bar { display: none; }
      .bp-page { background: white; color: black; border: 1.5px solid #000; box-shadow: none; margin-bottom: 0; padding: 12px; }
      .bp-title { color: #000; border-bottom: 2px solid #000; font-size: 1.25rem; }
      .bp-badge { color: #000; border: 1px solid #000; background: #eee; }
      .part-pill { background: #f8fafc; color: #000; border: 1px solid #ccc; border-left: 3px solid #000; }
      .part-pill strong { color: #000; }
    }
  </style>
</head>
<body>

  <div class="no-print-bar">
    <div>
      <h2 style="font-size:1.3rem; margin-bottom:4px;">Rayne's Printable Anatomical Atlas & Blueprint Pack</h2>
      <p style="color:#94a3b8; font-size:0.9rem;">Complete Labeled Plates & Blueprints for NBCC Practical Nursing Exam on Oct 13, 2026</p>
    </div>
    <button class="print-btn" onclick="window.print()">🖨️ Print / Save to PDF</button>
  </div>
"""

# Append Atlas Plates
for item in atlas_data:
    p_html = ""
    for p in item["parts"]:
        p_html += f"""
        <div class="part-pill">
          <strong>{p['name']}</strong>
          {p['role']}
        </div>
        """

    secondary_img = ""
    if item["img_secondary"]:
        secondary_img = f"""
        <div style="margin-top:8px;">
          <img src="{item['img_secondary']}?t=3" alt="{item['title']} View" style="max-width:100%; max-height:240px; height:auto; border-radius:4px; display:block; margin:0 auto;">
        </div>
        """

    printable_html += f"""
  <div class="bp-page">
    <div class="bp-title-row">
      <div class="bp-title">ATLAS: {item['title']}</div>
      <div class="bp-badge">{item['system']}</div>
    </div>
    <div class="bp-diagram-box">
      <img src="{item['img']}?t=3" alt="{item['title']}">
      {secondary_img}
    </div>
    <div class="parts-grid">
      {p_html}
    </div>
  </div>
"""

# Append Concept Blueprints
for mod in modules_data:
    printable_html += f"""
  <div class="bp-page">
    <div class="bp-title-row">
      <div class="bp-title">BLUEPRINT: {mod['title']}</div>
      <div class="bp-badge">{mod['chapter']}</div>
    </div>
    <div class="bp-diagram-box">
      <img src="{mod['diagram']}?t=3" alt="{mod['title']}">
    </div>
    <div style="background:#0f172a; padding:12px; border-radius:6px; font-size:0.88rem; border-left:4px solid #38bdf8;">
      <strong>High-Yield Scope:</strong> {mod['summary']}
    </div>
  </div>
"""

printable_html += """
</body>
</html>
"""

with open(os.path.join(base_dir, "Rayne_AP_Master_Blueprints_Printable_Modules_1_8.html"), "w", encoding="utf-8") as f:
    f.write(printable_html)

print("Updated Rayne_AP_Master_Blueprints_Printable_Modules_1_8.html with Atlas plates!")
