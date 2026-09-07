# Vibroacoustic Therapy Wearable - System Architecture

## Project Overview
A synchronized hardware and software system designed to induce specific emotional and autonomic nervous system responses via targeted vibroacoustic therapy. The system pairs auditory tones (binaural beats, isochronic tones) with localized haptic feedback at precise resonant frequencies along the spine and cranial nodes.

## 1. Hardware Architecture (The Vest & Headpiece)

### Core Processing & Connectivity
*   **Microcontroller:** ESP32 (WROOM or WROVER module)
    *   *Why:* Built-in Bluetooth Low Energy (BLE), dual-core processing for multi-thread timing, small footprint, low power consumption.
*   **Power Supply:** 3.7V Lithium-Polymer (LiPo) battery pack with a TP4056 charging and protection circuit.

### Actuation (Haptics)
*   **Motors:** Linear Resonant Actuators (LRAs)
    *   *Why:* Unlike standard Eccentric Rotating Mass (ERM) motors, LRAs oscillate on a single axis and can hit highly precise Hz frequencies with rapid start/stop times.
*   **Motor Drivers:** Texas Instruments DRV2605L Haptic Motor Drivers
    *   *Why:* Communicates with the ESP32 via I2C. Designed specifically to drive LRAs at resonant frequencies and can load pre-programmed waveforms.

### Form Factor & Wiring
*   **Material:** Breathable, compression neoprene to ensure actuators maintain tight skin contact.
*   **Wiring:** Conductive thread or flexible silicone-coated ribbon cables to prevent breakage during movement.

## 2. Software Architecture (The Mobile Application)

### Frontend App
*   **Framework:** React Native or Flutter for cross-platform (iOS/Android) compatibility.
*   **UI/UX:** Simple dashboard allowing users to select their desired emotional or physiological state (e.g., "Deep Focus", "Autonomic Down-regulation", "Anxiety Relief").

### Bluetooth & Trigger Protocol
*   **BLE Protocol:** The app acts as the BLE Central device, connecting to the ESP32 (Peripheral). 
*   **Data Packets:** When a state is selected, the app sends a specific byte array instructing the ESP32 *which* motor addresses to fire, at *what* frequency (Hz), and *when* (timing sequence).

### Audio Engine
*   **Tone Generation:** The app simultaneously plays the corresponding audio track (binaural beats or isochronic tones) through the user's Bluetooth or wired headphones, perfectly synchronized with the haptic firing sequence in the vest.

## 3. Biological & Somatic Parameters (Engineered by Soma)

### Anatomical Placement (The Nodes)
*Note on Placement Vector (The Elder's Input):* All somatic nodes (excluding the headpiece) are to be placed exclusively on the posterior (back) of the body, directly along the spine (*Sushumna Nadi*). This targets the unconscious/historical memory held in the back of the energetic centers, while allowing the physical resonance to carry through the skeletal structure to the front of the body. Frontal placement is unnecessary and counterproductive to the goal of deep historical awakening.

*   **The Headpiece (Vagus Nerve / Third Eye):** Targeted at the tragus of the ear for vagal down-regulation, with an optional node at the center of the brow (Ajna) for cosmic connection.
*   **Throat Center (C3-C5):** Pharyngeal plexus and thyroid stimulation (respiratory pacing).
*   **Heart Center (T1-T4):** Cardiac plexus. Helps regulate Heart Rate Variability (HRV) when paired with slow auditory pacing.
*   **Solar Plexus (T5-T9):** Celiac plexus and adrenal glands. The primary metabolic and stress-response hub.
*   **Root / Sacral (S1-S4):** Sacral plexus. Mechanically grounding, affecting the pelvic floor and lower-body proprioception.

### Frequency Engineering (Hz)
*   **30 - 50 Hz (Meissner's Corpuscles):** The optimal range for tactile flutter. **40 Hz** specifically induces Gamma wave neural synchronization for deep cognitive focus and neuro-protection.
*   **200 - 300 Hz (Pacinian Corpuscles):** Triggers a deep sensation of continuous pressure, masking localized pain and creating physical warmth/grounding.
*   **1 - 4 Hz (Delta Waves):** Sweeping low-frequency pulses down the spine to induce autonomic down-regulation for deep recovery and sleep.

## 4. Amplitude Calibration & Biological Guardrails

### Intensity Control
*   **Independent Modulation:** The DRV2605L motor drivers allow the software to control frequency (Hz) independently of amplitude (kinetic intensity). 
*   **User Calibration:** The app must feature an "Intensity Calibration" slider to accommodate varying body compositions (paraspinal muscle mass, adipose tissue), ensuring the mechanical wave successfully reaches the central nervous system without causing discomfort.

### Biological Guardrails (Safety Protocols)
*   **Sensory Habituation Cap:** The human nervous system habituates to constant mechanical stimuli in 15-20 minutes. Therefore, sessions must be hard-capped at 20 minutes to remain effective.
*   **Waveform Undulation:** The haptic software should utilize swelling, pulsing, and fading waveforms rather than a static drone to prevent the mechanoreceptors from tuning out the signal.
*   **Sympathetic Overdrive Prevention (The Jackhammer Effect):** Extreme mechanical vibration mimics environmental danger, spiking cortisol and adrenaline. The hardware must have a hard-coded maximum output limit to prevent the actuators from crossing the threshold from "deep resonance" into "violent shaking."

## 5. Garment Structure & Physical Blueprint

### The Vest (Main Chassis)
*   **Material:** Soft, breathable compression neoprene (similar to high-end athletic wear or scuba gear) for structural integrity and comfort.
*   **Posterior Profile (Supine Comfort):** The entire back panel is engineered to be perfectly flat and smooth. All actuators, wiring, and the ESP32 housing are recessed into insulated internal pockets so the user can comfortably lie flat on their back during sessions without pressure points.
*   **Spinal Channel & Tail:** Internally, the hardware runs the length of the spine, extending into a distinct "tail" section to cover the Sacral and Root ganglia (S1-S4) below the waistline.
*   **Adjustability System:** 
    *   **Side Panels:** Open sides secured by wide, industrial-grade Velcro straps (top, middle, and bottom) to wrap and tighten around various body types securely.
    *   **Shoulder Straps:** Adjustable Velcro shoulder points to raise or lower the spinal alignment based on torso length.

### The Ergonomic Cervical Neck Collar (v3 Specification)
*   **Structural Integration:** Replaces the full headpiece/skull cap with a high, contoured compression collar that seamlessly extends from the upper back panel up to the base of the skull (occiput / C1-C7 cervical vertebrae).
*   **Headphone Clearance:** Leaves the head, crown, and ears 100% uncovered and unobstructed, allowing users to wear any over-ear audiophile headphones (Bose, Sony, AirPods Max) or spatial sound systems with zero physical crowding.
*   **Anatomical & Vagal Targeting:** Haptic LRA transducers are positioned at the suboccipital ridge (C1-C2 atlas-axis) and cervical spine (C3-C7). Mechanical vibration transmits directly via bone conduction into the cranial base, stimulating the Vagus Nerve and Reticular Activating System (RAS).

