import os
import textwrap
import matplotlib.pyplot as plt
import matplotlib.patches as patches

img_dir = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC/images"
os.makedirs(img_dir, exist_ok=True)

def draw_card(ax, x, y, w, h, title, bullets, border_color, header_bg, body_bg, header_text_color='white'):
    # Card outer box with rounded corners
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", 
                                facecolor=body_bg, edgecolor=border_color, linewidth=2.2, zorder=2)
    ax.add_patch(box)
    
    # Header banner at the top of the card
    header_h = 0.62
    header_box = patches.FancyBboxPatch((x, y + h - header_h), w, header_h, boxstyle="round,pad=0.04",
                                        facecolor=header_bg, edgecolor=border_color, linewidth=1.5, zorder=3)
    ax.add_patch(header_box)
    
    # Header title
    ax.text(x + w / 2.0, y + h - (header_h / 2.0), title, fontsize=9.2, fontweight='heavy',
            color=header_text_color, ha='center', va='center', zorder=4)
    
    # Format and wrap bullet points
    wrapped_lines = []
    for b in bullets:
        if b.strip():
            lines = textwrap.wrap(b, width=48, subsequent_indent="   ")
            wrapped_lines.extend(lines)
        else:
            wrapped_lines.append("")
            
    full_text = "\n".join(wrapped_lines)
    
    # Body text placement
    text_x = x + 0.26
    text_y = y + h - header_h - 0.20
    ax.text(text_x, text_y, full_text, fontsize=7.3, color='#0f172a',
            va='top', ha='left', linespacing=1.24, fontweight='medium', zorder=4)

def setup_canvas(title_text):
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    canvas = patches.FancyBboxPatch((0.2, 0.2), 11.6, 8.1, boxstyle="round,pad=0.15",
                                   facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=2.5, zorder=1)
    ax.add_patch(canvas)

    plt.title(title_text, fontsize=13, fontweight='bold', color='#0f172a', pad=14)
    return fig, ax

# Geometry constants
card_w = 5.45
card_h = 3.55
y_top = 4.45
y_bottom = 0.52
x_left = 0.42
x_right = 6.12

# -------------------------------------------------------------
# 1. MODULE 1: ANATOMICAL PLANES, CAVITIES & HOMEOSTASIS
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 1 BLUEPRINT: ANATOMICAL PLANES, CAVITIES & HOMEOSTASIS")

b1 = [
    "• Superior (Cranial): Toward the head / upper body",
    "• Inferior (Caudal): Away from head / lower body",
    "• Anterior (Ventral): Toward the front of the body",
    "• Posterior (Dorsal): Toward the back of the body",
    "• Medial: Closer to the midline of the body",
    "• Lateral: Farther away from the body midline",
    "• Proximal: Closer to trunk / point of attachment",
    "• Distal: Farther from trunk / point of attachment",
    "• Superficial: Toward the surface | Deep: Internal"
]
draw_card(ax, x_left, y_top, card_w, card_h, "DIRECTIONAL TERMINOLOGY", b1,
          '#1e40af', '#1e40af', '#eff6ff')

b2 = [
    "• Sagittal Plane: Divides body into Right & Left",
    "  - Midsagittal: Exactly equal right & left halves",
    "  - Parasagittal: Unequal right & left portions",
    "• Frontal (Coronal) Plane: Divides into Anterior",
    "  (front) and Posterior (back) portions",
    "• Transverse (Horizontal) Plane: Divides into",
    "  Superior (upper) and Inferior (lower) parts",
    "• Oblique Plane: Diagonal cut between horizontal",
    "  and vertical planes"
]
draw_card(ax, x_right, y_top, card_w, card_h, "BODY PLANES & SECTIONS", b2,
          '#9d174d', '#9d174d', '#fdf2f8')

b3 = [
    "1. DORSAL CAVITY (Posterior aspect):",
    "   • Cranial Cavity: Houses the brain",
    "   • Spinal (Vertebral) Cavity: Houses spinal cord",
    "2. VENTRAL CAVITY (Anterior aspect):",
    "   • Thoracic: Pleural (lungs), Pericardial (heart),",
    "     and Mediastinum (central trachea/esophagus)",
    "   • Diaphragm: Muscular partition dividing cavities",
    "   • Abdominopelvic: Abdominal (digestive organs)",
    "     and Pelvic (bladder & reproductive organs)"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "BODY CAVITIES ARCHITECTURE", b3,
          '#166534', '#166534', '#f0fdf4')

b4 = [
    "• Negative Feedback (Predominant Mechanism):",
    "  - REVERSES deviation back toward normal set point",
    "  - Pathway: Sensor -> Control Center -> Effector",
    "  - Clinical Examples: Thermoregulation, Blood Glucose",
    "• Positive Feedback (Rare & Temporary):",
    "  - AMPLIFIES deviation away from set point to",
    "    accelerate event to definitive completion",
    "  - Clinical Examples: Oxytocin in labor childbirth,",
    "    Platelet plug & blood clotting cascade"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "HOMEOSTATIC FEEDBACK LOOPS", b4,
          '#b45309', '#b45309', '#fffbeb')

plt.savefig(os.path.join(img_dir, "mod1_anatomical_planes_cavities.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 2. MODULE 2: CELL ORGANELLES & TRANSPORT DYNAMICS
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 2 BLUEPRINT: THE CELL, ORGANELLES & TRANSPORT DYNAMICS")

b1 = [
    "• Nucleus: 'Control center' containing DNA chromatin",
    "• Mitochondria: 'Powerhouse' aerobic ATP synthesis",
    "• Ribosomes: Protein factories (free or on Rough ER)",
    "• Endoplasmic Reticulum (ER):",
    "  - Rough: Protein folding & transport with ribosomes",
    "  - Smooth: Lipid/steroid synthesis & drug detox",
    "• Golgi Apparatus: Packaging, sorting & secretion",
    "• Lysosomes: 'Digestive bags' with hydrolytic enzymes",
    "• Centrioles: Organize spindle fibers in mitosis"
]
draw_card(ax, x_left, y_top, card_w, card_h, "PRIMARY ORGANELLES & FUNCTIONS", b1,
          '#1d4ed8', '#1d4ed8', '#eff6ff')

b2 = [
    "• Phospholipid Bilayer (Fluid Mosaic Model):",
    "  - Hydrophilic heads (polar) face outer/inner fluid",
    "  - Hydrophobic tails (fatty acids) face inward core",
    "• Embedded Proteins: Receptors, channels, carriers",
    "• Cholesterol: Maintains flexibility & stability",
    "• Selective Permeability: Regulates passage of ions",
    "  and water-soluble macromolecules into cytoplasm"
]
draw_card(ax, x_right, y_top, card_w, card_h, "PLASMA MEMBRANE (LIPID BILAYER)", b2,
          '#6b21a8', '#6b21a8', '#faf5ff')

b3 = [
    "• Diffusion: Solutes move HIGH -> LOW concentration",
    "• Osmosis: Water moves across membrane down water",
    "  concentration gradient (toward higher solute)",
    "• Filtration: Driven by HYDROSTATIC pressure gradient",
    "  (e.g., blood pressure pushing across glomerulus)",
    "• Tonicity Effects on Red Blood Cells:",
    "  - Isotonic (0.9% NaCl): Zero net water movement",
    "  - Hypertonic: Water leaves cell -> CRENATION (shrivel)",
    "  - Hypotonic: Water enters cell -> SWELLS & LYSES"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "PASSIVE TRANSPORT (NO ATP)", b3,
          '#15803d', '#15803d', '#f0fdf4')

b4 = [
    "• Active Transport: Requires ATP (Against gradient)",
    "  - Na+/K+ ATPase Pump: 3 Na+ pumped OUT, 2 K+ IN",
    "  - Phagocytosis: Cell eating (engulfing bacteria)",
    "  - Pinocytosis: Cell drinking (fluid droplets)",
    "  - Exocytosis: Vesicles fuse to expel substances",
    "• Mitosis Phases (PMAT):",
    "  - Prophase (condense) -> Metaphase (align middle)",
    "  - Anaphase (pull apart) -> Telophase (reform)"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "ACTIVE TRANSPORT & CELL DIVISION", b4,
          '#be123c', '#be123c', '#fff1f2')

plt.savefig(os.path.join(img_dir, "mod2_cell_organelles_transport.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 3. MODULE 3: INTEGUMENTARY ANATOMY, GLANDS & BURNS
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 3 BLUEPRINT: INTEGUMENTARY ANATOMY, GLANDS & BURNS")

b1 = [
    "1. EPIDERMIS (Avascular Stratified Squamous):",
    "   • 95% Keratinocytes (waterproofing keratin)",
    "   • 5% Melanocytes (melanin UV shield in basale)",
    "   • 5 Strata (deep to superficial): Basale (mitosis),",
    "     Spinosum, Granulosum, Lucidum (thick skin), Corneum",
    "2. DERMIS (Vascular Connective Tissue - 20x thicker):",
    "   • Papillary Layer: Dermal papillae & Meissner corpuscles",
    "   • Reticular Layer: Dense collagen, vessels & Pacinian",
    "3. HYPODERMIS: Adipose cushion, energy storage & insulation"
]
draw_card(ax, x_left, y_top, card_w, card_h, "3 PRIMARY LAYERS OF SKIN", b1,
          '#9d174d', '#9d174d', '#fdf2f8')

b2 = [
    "• Sebaceous (Oil) Glands: Holocrine glands secreting",
    "  sebum into hair follicles (lubricates, antibacterial)",
    "• Sudoriferous (Sweat) Glands:",
    "  - Eccrine: Watery perspiration over whole body for",
    "    thermoregulation; exits skin pores directly",
    "  - Apocrine: Axillary & genital regions; thick secretion",
    "    activated at puberty; bacterial breakdown causes odor",
    "• Arrector Pili: Smooth muscle causing goosebumps"
]
draw_card(ax, x_right, y_top, card_w, card_h, "CUTANEOUS GLANDS & APPENDAGES", b2,
          '#1d4ed8', '#1d4ed8', '#eff6ff')

b3 = [
    "• Protection: Physical barrier vs. pathogens & UV",
    "• Thermoregulation:",
    "  - Excessive Heat: Dermal vasodilation & eccrine sweat",
    "  - Cold Exposure: Dermal vasoconstriction & shivering",
    "• Sensory Reception: Meissner (touch), Pacinian (pressure),",
    "  Free nerve endings (pain & temperature)",
    "• Excretion: Minor waste elimination (urea, salts, water)",
    "• Synthesis: Vitamin D precursor activated by UV sunlight"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "KEY PHYSIOLOGICAL FUNCTIONS", b3,
          '#15803d', '#15803d', '#f0fdf4')

b4 = [
    "• Burn Depths & Characteristics:",
    "  - 1st Degree: Epidermis only (redness, pain, sunburn)",
    "  - 2nd Degree: Epidermis + upper dermis (blisters, pain)",
    "  - 3rd Degree: Full thickness (charred/white, nerves",
    "    destroyed, painless in immediate center)",
    "• Adult Rule of Nines (Total Body Surface Area):",
    "  - Head & Neck: 9% | Entire Arm: 9% each",
    "  - Anterior Trunk: 18% | Posterior Trunk: 18%",
    "  - Entire Leg: 18% each | Perineum (genitals): 1%"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "BURNS & RULE OF NINES", b4,
          '#c2410c', '#c2410c', '#fff7ed')

plt.savefig(os.path.join(img_dir, "mod3_skin_layers_appendages.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 4. MODULE 4: SKELETAL HISTOLOGY, AXES & ARTICULATIONS
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 4 BLUEPRINT: SKELETAL HISTOLOGY, AXES & ARTICULATIONS")

b1 = [
    "• Osteon (Haversian System): Compact bone unit",
    "  - Lamellae: Concentric mineralized rings",
    "  - Central Canal: Neurovascular bundle",
    "  - Lacunae: Chambers housing osteocytes",
    "  - Canaliculi: Microscopic transport canals",
    "• Triad of Bone Cells:",
    "  - Osteoblasts: Bone BUILDERS (calcification)",
    "  - Osteoclasts: Bone REABSORBERS (breakdown)",
    "  - Osteocytes: Mature cells maintaining matrix"
]
draw_card(ax, x_left, y_top, card_w, card_h, "BONE CELLS & HISTOLOGY (OSTEON)", b1,
          '#1d4ed8', '#1d4ed8', '#eff6ff')

b2 = [
    "• Diaphysis: Hollow shaft of compact bone",
    "• Epiphyses: Ends with spongy bone & red marrow",
    "• Epiphyseal Plate: Cartilage growth plate",
    "  (ossifies into Epiphyseal Line in adults)",
    "• Articular Cartilage: Hyaline cushion on joints",
    "• Periosteum: Fibrous outer vascular membrane",
    "• Endosteum: Inner membrane of medullary cavity",
    "• Medullary Cavity: Contains yellow fat marrow"
]
draw_card(ax, x_right, y_top, card_w, card_h, "MACROSCOPIC LONG BONE STRUCTURE", b2,
          '#b45309', '#b45309', '#fffbeb')

b3 = [
    "1. AXIAL SKELETON (80 Bones - Central Axis):",
    "   • Skull: Cranial (8) & Facial (14)",
    "   • Spine: 7 Cervical, 12 Thoracic, 5 Lumbar,",
    "     Sacrum & Coccyx",
    "   • Thoracic Cage: Sternum + 12 pairs ribs",
    "     (7 True, 3 False, 2 Floating)",
    "2. APPENDICULAR SKELETON (126 Bones - Limbs):",
    "   • Pectoral Girdle: Clavicle & Scapula",
    "   • Upper Limbs: Humerus, Radius, Ulna, Carpals",
    "   • Pelvic Girdle: Coxal bones (Ilium, Ischium)",
    "   • Lower Limbs: Femur, Patella, Tibia, Fibula"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "AXIAL VS. APPENDICULAR SKELETON", b3,
          '#7e22ce', '#7e22ce', '#faf5ff')

b4 = [
    "• Synarthroses (Immovable): Cranial sutures",
    "• Amphiarthroses (Slightly Movable):",
    "  - Symphysis pubis & Intervertebral discs",
    "• Diarthroses (Freely Movable Synovial Joints):",
    "  - Ball-and-Socket: Hip, Shoulder (widest ROM)",
    "  - Hinge: Knee, Elbow (flexion / extension)",
    "  - Pivot: Atlas / Axis (C1 / C2 head rotation)",
    "  - Saddle: Thumb carpometacarpal joint",
    "  - Condyloid & Gliding (plane) joints"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "JOINT CLASSIFICATIONS (ARTICULATIONS)", b4,
          '#059669', '#059669', '#ecfdf5')

plt.savefig(os.path.join(img_dir, "mod4_skeletal_osteon_divisions.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 5. MODULE 5: MUSCLE ULTRASTRUCTURE & CONTRACTION MECHANICS
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 5 BLUEPRINT: MUSCLE ULTRASTRUCTURE & CONTRACTION MECHANICS")

b1 = [
    "• Skeletal Muscle: Striated, Voluntary, Multinucleated,",
    "  attached to bones, produces movement & heat",
    "• Cardiac Muscle: Striated, Involuntary, Single nucleus,",
    "  INTERCALATED DISCS (gap junctions for electrical syncytium)",
    "• Smooth Muscle: Non-striated, Involuntary, Spindle-shaped,",
    "  walls of hollow organs & vessels, sustained tone",
    "• Connective Fascia: Epimysium (entire muscle) ->",
    "  Perimysium (fascicles) -> Endomysium (fibers)"
]
draw_card(ax, x_left, y_top, card_w, card_h, "3 MUSCLE TISSUE TYPES", b1,
          '#1d4ed8', '#1d4ed8', '#eff6ff')

b2 = [
    "• Sarcomere: Contractile functional unit between Z-lines",
    "• Myofilaments:",
    "  - Thick Filaments: MYOSIN with pivoting heads",
    "  - Thin Filaments: ACTIN, Troponin & Tropomyosin",
    "• Contraction Steps:",
    "  1. Action potential triggers ACh release at NMJ",
    "  2. Sarcoplasmic reticulum releases CALCIUM (Ca2+)",
    "  3. Ca2+ binds Troponin -> shifts Tropomyosin",
    "  4. Myosin heads bind Actin -> Power stroke pulls Z-lines",
    "  5. ATP binds to detach & reset myosin head"
]
draw_card(ax, x_right, y_top, card_w, card_h, "SARCOMERE SLIDING FILAMENT THEORY", b2,
          '#be123c', '#be123c', '#fdf2f8')

b3 = [
    "• Prime Mover (Agonist): Main muscle for action",
    "  (e.g., Biceps brachii in elbow flexion)",
    "• Antagonist: Muscle that OPPOSES prime mover",
    "  (e.g., Triceps brachii relaxes during elbow flexion)",
    "• Synergist: Assists prime mover & stabilizes motion",
    "• Fixator: Stabilizes bone of origin",
    "• Attachments:",
    "  - Origin: Stationary bone attachment point",
    "  - Insertion: Movable bone attachment point"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "FUNCTIONAL ROLES & LEVERAGE", b3,
          '#15803d', '#15803d', '#f0fdf4')

b4 = [
    "• Isotonic Contraction: Muscle changes length, tension constant",
    "  - Concentric: Muscle SHORTENS (lifting dumbbell)",
    "  - Eccentric: Muscle LENGTHENS under load (lowering)",
    "• Isometric Contraction: Tension increases, length UNCHANGED",
    "  (e.g., pushing wall, holding plank, maintaining posture)",
    "• Muscle Tone: Constant slight state of partial contraction",
    "• Fatigue & Oxygen Debt: Lactic acid accumulation when",
    "  aerobic ATP depleted during intense anaerobic effort"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "CONTRACTION TYPES & FATIGUE", b4,
          '#b45309', '#b45309', '#fffbeb')

plt.savefig(os.path.join(img_dir, "mod5_muscle_sarcomere_contraction.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 6. MODULE 6: NERVOUS TRANSMISSION, REFLEXES & ANS
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 6 BLUEPRINT: NERVOUS TRANSMISSION, REFLEXES & ANS ARCHITECTURE")

b1 = [
    "• Neuron Anatomy: Dendrites (receive), Soma (cell body),",
    "  Axon (conducts away), Myelin Sheath (insulates)",
    "• Neuroglial Cells (Supporting Glia):",
    "  - Astrocytes: Forms Blood-Brain Barrier (BBB)",
    "  - Microglia: Resident CNS phagocytes cleaning debris",
    "  - Oligodendrocytes: Produces myelin sheaths in CNS",
    "  - Schwann Cells: Produces myelin sheaths in PNS",
    "  - Ependymal Cells: Lines ventricles & circulates CSF"
]
draw_card(ax, x_left, y_top, card_w, card_h, "NEURONS & NEUROGLIAL SUPPORT", b1,
          '#1d4ed8', '#1d4ed8', '#eff6ff')

b2 = [
    "• Resting State: -70 mV (High Na+ Outside, High K+ Inside)",
    "• Depolarization: Threshold stimulus opens Na+ gates",
    "  -> Rapid Sodium INFLUX into cell (+30 mV)",
    "• Repolarization: K+ channels open -> Potassium EFFLUX",
    "• Na+/K+ Pump: Restores original ionic concentrations",
    "• Saltatory Conduction: Impulse jumps across Nodes of",
    "  Ranvier, dramatically accelerating conduction velocity",
    "• Synaptic Transmission: Exocytosis of neurotransmitters"
]
draw_card(ax, x_right, y_top, card_w, card_h, "ACTION POTENTIAL & SYNAPSE", b2,
          '#6b21a8', '#6b21a8', '#faf5ff')

b3 = [
    "1. Sensory Receptor: Detects stimulus (heat, pain, stretch)",
    "2. Sensory (Afferent) Neuron: Transmits impulse to CNS",
    "3. Integration Center: Interneuron within spinal cord gray",
    "   matter coordinates reflex response",
    "4. Motor (Efferent) Neuron: Conducts impulse out to effector",
    "5. Effector Organ: Muscle contracts or gland secretes",
    "• Monosynaptic (Patellar Knee-Jerk): No interneuron",
    "• Polysynaptic (Withdrawal Reflex): Involves interneurons"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "5-STEP REFLEX ARC", b3,
          '#15803d', '#15803d', '#f0fdf4')

b4 = [
    "• Brainstem (Medulla Oblongata): Vital cardiac, vasomotor,",
    "  and respiratory control centers for survival",
    "• Cerebellum: Coordination, smooth motor control & balance",
    "• Hypothalamus: Master autonomic & endocrine regulator",
    "• Autonomic Nervous System (ANS) Divisions:",
    "  - Sympathetic: 'Fight or Flight' (thoracolumbar, high HR)",
    "  - Parasympathetic: 'Rest & Digest' (craniosacral, vagus",
    "    nerve, stimulates digestion & lowers HR)"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "BRAIN STEM & AUTONOMIC DIVISIONS", b4,
          '#be123c', '#be123c', '#fff1f2')

plt.savefig(os.path.join(img_dir, "mod6_nervous_reflex_arc.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 7. MODULE 7: SPECIAL SENSES (EYE, EAR & EQUILIBRIUM)
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 7 BLUEPRINT: SPECIAL SENSES — VISION, AUDITORY & EQUILIBRIUM")

b1 = [
    "1. Fibrous Tunic (Outer):",
    "   • Sclera: Tough, white protective coat of eyeball",
    "   • Cornea: Transparent anterior window; refracts light",
    "2. Vascular Tunic (Middle / Uvea):",
    "   • Choroid: Pigmented vascular layer absorbs excess light",
    "   • Ciliary Body: Muscle changes lens shape (accommodation)",
    "   • Iris: Smooth muscle ring controlling pupil aperture",
    "3. Sensory Tunic (Inner): RETINA with photoreceptors"
]
draw_card(ax, x_left, y_top, card_w, card_h, "VISION & THREE EYE TUNICS", b1,
          '#1d4ed8', '#1d4ed8', '#eff6ff')

b2 = [
    "• Rods: Dim light / night vision, peripheral fields, black/white",
    "• Cones: Bright light, color vision, sharp visual acuity",
    "• Fovea Centralis: Pit in macula lutea with highest cone density",
    "• Optic Disc: 'Blind Spot' (no photoreceptors, CN II exits)",
    "• Eye Cavities & Humors:",
    "  - Aqueous Humor: Watery anterior fluid; Canal of Schlemm",
    "    blockage causes GLAUCOMA (elevated intraocular pressure)",
    "  - Vitreous Humor: Gel-like posterior mass preventing collapse"
]
draw_card(ax, x_right, y_top, card_w, card_h, "PHOTORECEPTORS & EYE CAVITIES", b2,
          '#854d0e', '#854d0e', '#fefce8')

b3 = [
    "• External Ear: Auricle/Pinna & External auditory canal",
    "• Tympanic Membrane (Eardrum): Converts sounds to vibrations",
    "• Middle Ear: 3 Auditory Ossicles (Malleus -> Incus -> Stapes)",
    "  - Eustachian Tube: Equalizes pressure with nasopharynx",
    "• Inner Ear (Cochlea):",
    "  - Stapes pushes Oval Window -> fluid waves in perilymph",
    "  - ORGAN OF CORTI: Hair cells deflect against tectorial",
    "    membrane -> generates impulses via CN VIII"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "EAR ANATOMY & AUDITORY PATHWAY", b3,
          '#9d174d', '#9d174d', '#fdf2f8')

b4 = [
    "• Static Equilibrium: VESTIBULE (Utricle & Saccule with Otoliths)",
    "  - Senses head position relative to gravity & linear movement",
    "• Dynamic Equilibrium: SEMICIRCULAR CANALS (Crista ampullaris)",
    "  - Senses rotational & angular head acceleration in 3 planes",
    "• Olfaction (Smell): Chemoreceptors in upper nasal mucosa (CN I)",
    "• Gustation (Taste): Chemoreceptors in taste buds (sweet, sour,",
    "  salty, bitter, umami) carried by CN VII & CN IX"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "EQUILIBRIUM, TASTE & SMELL", b4,
          '#065f46', '#065f46', '#ecfdf5')

plt.savefig(os.path.join(img_dir, "mod7_special_senses_eye_ear.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 8. MODULE 8: ENDOCRINE GLANDS & METABOLIC AXES
# -------------------------------------------------------------
fig, ax = setup_canvas("MODULE 8 BLUEPRINT: ENDOCRINE GLANDS, HORMONES & METABOLIC AXES")

b1 = [
    "• Endocrine vs. Exocrine:",
    "  - Endocrine: DUCTLESS glands secreting hormones into blood",
    "  - Exocrine: Secrete through DUCTS onto surfaces (sweat)",
    "• Protein / Nonsteroid Hormones: Water-soluble;",
    "  First messenger binds membrane surface receptor -> activates",
    "  Second Messenger (cyclic AMP / cAMP) inside cytoplasm",
    "• Steroid Hormones: Lipid-soluble; diffuse across membrane,",
    "  bind intracellular receptors & directly alter DNA transcription"
]
draw_card(ax, x_left, y_top, card_w, card_h, "ENDOCRINE GLANDS & HORMONE TYPES", b1,
          '#1d4ed8', '#1d4ed8', '#eff6ff')

b2 = [
    "• Anterior Pituitary (Adenohypophysis - Master Gland):",
    "  - TSH (Thyroid), ACTH (Adrenal cortex), FSH & LH (Gonads),",
    "    GH (Growth hormone), PRL (Prolactin for lactation)",
    "• Posterior Pituitary (Neurohypophysis - Storage):",
    "  - ADH (Vasopressin): Kidney water retention (concentrates urine)",
    "  - Oxytocin: Uterine contractions in labor & milk let-down",
    "  * Both synthesized by HYPOTHALAMUS and stored here"
]
draw_card(ax, x_right, y_top, card_w, card_h, "HYPOTHALAMUS & PITUITARY AXIS", b2,
          '#6b21a8', '#6b21a8', '#faf5ff')

b3 = [
    "• Thyroid Gland:",
    "  - T3 & T4 (requires dietary Iodine): Regulates basal metabolism",
    "  - Calcitonin: LOWERS blood calcium ('tones down' calcium)",
    "    Inhibits osteoclasts & stimulates osteoblast bone storage",
    "• Parathyroid Glands (PTH):",
    "  - RAISES blood calcium: Stimulates osteoclasts to breakdown",
    "    bone, increases renal Ca2+ reabsorption & activates Vitamin D",
    "  * Calcitonin & PTH are ANTAGONISTIC homeostatic hormones"
]
draw_card(ax, x_left, y_bottom, card_w, card_h, "THYROID, PARATHYROID & CALCIUM", b3,
          '#15803d', '#15803d', '#f0fdf4')

b4 = [
    "• Pancreas (Islets of Langerhans Glucose Homeostasis):",
    "  - Beta Cells: INSULIN (Lowers glucose -> glycogen storage)",
    "  - Alpha Cells: GLUCAGON (Raises glucose -> glycogenolysis)",
    "• Adrenal Cortex: Aldosterone (Na+ retention, K+ excretion);",
    "  Cortisol (Stress response, glucose elevation, anti-inflammatory)",
    "• Adrenal Medulla: Epinephrine / Norepinephrine (Fight or Flight)",
    "• Pineal Gland: Melatonin (Circadian sleep-wake rhythm)",
    "• Thymus Gland: Thymosin (T-lymphocyte immune programming)"
]
draw_card(ax, x_right, y_bottom, card_w, card_h, "PANCREAS & ADRENAL HORMONES", b4,
          '#c2410c', '#c2410c', '#fff7ed')

plt.savefig(os.path.join(img_dir, "mod8_endocrine_axis_feedback.png"), bbox_inches='tight', dpi=300)
plt.close()

print("ALL 8 MODULE BLUEPRINT DIAGRAMS SUCCESSFULLY REGENERATED WITH FLAWLESS MARGINS!")
