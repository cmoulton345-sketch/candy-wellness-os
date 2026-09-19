import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

img_dir = "/Users/valuedcustomer/Downloads/flowstate_ai_os_candy/Rayne_NBCC/images"
os.makedirs(img_dir, exist_ok=True)

# --- DIAGRAM 1: THE HUMAN CELL DIAGRAM ---
fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')

cell_outer = patches.Circle((0, 0), 1.0, facecolor='#e0f2fe', edgecolor='#0284c7', linewidth=4)
ax.add_patch(cell_outer)

nucleus = patches.Circle((0, 0), 0.4, facecolor='#fbcfe8', edgecolor='#be185d', linewidth=3)
ax.add_patch(nucleus)

mito1 = patches.Ellipse((-0.6, 0.5), 0.35, 0.18, angle=30, facecolor='#fef08a', edgecolor='#ca8a04', linewidth=2)
mito2 = patches.Ellipse((0.6, -0.4), 0.35, 0.18, angle=-20, facecolor='#fef08a', edgecolor='#ca8a04', linewidth=2)
ax.add_patch(mito1)
ax.add_patch(mito2)

np.random.seed(42)
rx = np.random.uniform(-0.8, 0.8, 40)
ry = np.random.uniform(-0.8, 0.8, 40)
r_mask = (rx**2 + ry**2 < 0.85) & (rx**2 + ry**2 > 0.45)
ax.scatter(rx[r_mask], ry[r_mask], color='#475569', s=25, zorder=4)

ax.text(0, 0, 'NUCLEUS\n(DNA & Chromosomes)', color='#831843', fontsize=10, fontweight='bold', ha='center', va='center')
ax.text(-0.6, 0.65, 'Mitochondria\n(ATP Energy)', color='#854d0e', fontsize=8.5, fontweight='bold', ha='center')
ax.text(0.65, -0.6, 'Mitochondria\n(ATP Energy)', color='#854d0e', fontsize=8.5, fontweight='bold', ha='center')
ax.text(0.7, 0.75, 'Plasma Membrane\n(Lipid Bilayer)', color='#0369a1', fontsize=9.5, fontweight='bold', ha='center')
ax.text(-0.7, -0.75, 'Cytoplasm\n(Gel Fluid)', color='#0f766e', fontsize=9.5, fontweight='bold', ha='center')

plt.title('ANATOMICAL BLUEPRINT 1: THE HUMAN CELL STRUCTURE', fontsize=13, fontweight='bold', color='#0f172a', pad=12)
cell_img_path = os.path.join(img_dir, "cell_diagram.png")
plt.savefig(cell_img_path, bbox_inches='tight', dpi=300)
plt.close()

# --- DIAGRAM 2: INTEGUMENTARY SYSTEM SKIN LAYERS ---
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Epidermis
ax.add_patch(patches.Rectangle((1, 7.3), 8, 2.2, facecolor='#fbcfe8', edgecolor='#9d174d', linewidth=2))
ax.text(1.2, 8.4, 'EPIDERMIS (Outermost Layer)\n• Nonvascular (No Blood Vessels)\n• 95% Keratinocytes (Waterproof) | 5% Melanocytes (Melanin Pigment)\n• 5 Strata: Basale, Spinosum, Granulosum, Lucidum, Corneum', fontsize=9.5, color='#831843', va='center')

# Dermis
ax.add_patch(patches.Rectangle((1, 3.5), 8, 3.5, facecolor='#bae6fd', edgecolor='#0369a1', linewidth=2))
ax.text(1.2, 5.25, 'DERMIS (Middle Layer - 20x Thicker)\n• Papillary Layer: Dermal Papillae (Fingerprints) & Touch Receptors\n• Reticular Layer: Collagen & Elastic Fibers, Blood Vessels, Hair Follicles\n• Cutaneous Receptors: Meissner, Pacinian, Krause, Ruffini, Free Nerve Endings', fontsize=9.5, color='#0c4a6e', va='center')

# Hypodermis
ax.add_patch(patches.Rectangle((1, 0.8), 8, 2.4, facecolor='#fef08a', edgecolor='#ca8a04', linewidth=2))
ax.text(1.2, 2.0, 'HYPODERMIS / SUBCUTANEOUS (Foundation Layer)\n• Adipose (Fat) Tissue\n• Functions: Thermal Insulation, Energy Storage, Cushioning\n• Anchors Skin to Underlying Muscles & Bones', fontsize=9.5, color='#713f12', va='center')

plt.title('ANATOMICAL BLUEPRINT 2: SKIN LAYERS & STRUCTURE', fontsize=13, fontweight='bold', color='#0f172a', pad=12)
skin_img_path = os.path.join(img_dir, "skin_diagram.png")
plt.savefig(skin_img_path, bbox_inches='tight', dpi=300)
plt.close()

# --- DIAGRAM 3: SKELETAL SYSTEM BREAKDOWN ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)

divisions = ['Axial Skeleton\n(80 Bones)', 'Appendicular Skeleton\n(126 Bones)']
counts = [80, 126]
colors = ['#0284c7', '#e11d48']

ax1.bar(divisions, counts, color=colors, width=0.5, edgecolor='#0f172a', linewidth=1.5)
ax1.set_ylabel('Number of Bones', fontsize=10, fontweight='bold')
ax1.set_title('Skeleton Divisions (206 Total)', fontsize=11, fontweight='bold', color='#0f172a')
ax1.set_ylim(0, 145)
for i, v in enumerate(counts):
    ax1.text(i, v + 4, f'{v} Bones', ha='center', fontweight='bold', fontsize=10)

btypes = ['Long', 'Short', 'Flat', 'Irregular', 'Sesamoid']
examples = ['Femur', 'Carpals', 'Sternum', 'Vertebra', 'Patella']
x_pos = np.arange(len(btypes))

ax2.bar(x_pos, [5, 4, 4, 3, 2], color='#0d9488', edgecolor='#0f172a', linewidth=1.5)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(btypes, fontsize=9.5, fontweight='bold')
ax2.set_title('5 Bone Classifications & Examples', fontsize=11, fontweight='bold', color='#0f172a')
ax2.set_yticks([])
for i, ex in enumerate(examples):
    ax2.text(i, 0.4, ex, ha='center', va='bottom', color='white', fontweight='bold', fontsize=9.5, rotation=90)

plt.suptitle('ANATOMICAL BLUEPRINT 3: SKELETAL SYSTEM BREAKDOWN', fontsize=13, fontweight='bold', color='#0f172a', y=1.02)
skel_img_path = os.path.join(img_dir, "skel_diagram.png")
plt.savefig(skel_img_path, bbox_inches='tight', dpi=300)
plt.close()

print("Successfully generated all diagrams!")
