# Vibroacoustic Therapy Wearable - Solfeggio Audio-Haptic Frequency Matrix

## Overview
This document specifies the mathematical and physiological bridge between auditory Solfeggio frequencies played via headphones and tactile haptic oscillations delivered along the spinal column and suboccipital neck collar.

---

## 1. Somatosensory Engineering Principle

### Mechanoreceptor Frequency Bandwidth
Human tactile mechanoreceptors perceive vibrational stimuli optimally within specific frequency windows:
*   **Meissner's Corpuscles (30 - 50 Hz):** Responds to tactile flutter and low-frequency pulses. Ideal for 40 Hz Gamma entrainment.
*   **Pacinian Corpuscles (100 - 300 Hz):** Highly sensitive to rapid mechanical vibration. Peak sensitivity occurs around **150 - 250 Hz**.
*   **Tactile Insensitivity Threshold (> 350 Hz):** Above ~350 Hz, skin mechanoreceptors become insensitive to mechanical movement, and small Linear Resonant Actuators (LRAs) lose kinetic amplitude.

### The Harmonic Sub-Octave Solution
To maintain 1:1 acoustic-haptic synchronization when playing high Solfeggio audio frequencies (such as 528 Hz, 741 Hz, or 963 Hz), the haptic motor controller drives the LRAs at **harmonic sub-octaves** ($f_{haptic} = f_{audio} / 2^n$) falling directly within the Pacinian corpuscle sweet spot (100 - 200 Hz).

---

## 2. The 7 Solfeggio Audio-Haptic Mapping Matrix

| Node | Anatomical Location | Spinal Segment | Solfeggio Audio Tone | Primary Intended Effect | Haptic Motor Freq | Sub-Octave Formula |
|:---:|:---|:---|:---:|:---|:---:|:---:|
| **7** | **Suboccipital Base of Skull** | C1 - C2 (Occiput) | **963 Hz** | Higher Awareness & Spiritual Connection | **120.38 Hz** | $963 / 8$ |
| **6** | **Cervical Neck Collar** | C3 - C7 Cervical | **741 Hz** | Awakening Intuition & Mental Clarity | **92.63 Hz** | $741 / 8$ |
| **5** | **Heart Center** | T1 - T4 Thoracic | **528 Hz** | Miracle Tone, Transformation & Love | **132.00 Hz** | $528 / 4$ |
| **4** | **Mid-Thoracic / Solar** | T5 - T8 Thoracic | **432 Hz** | Natural Harmony & Heart Chakra Alignment | **108.00 Hz** | $432 / 4$ |
| **3** | **Solar Plexus / Adrenals** | T9 - T12 Thoracic | **417 Hz** | Clearing Trauma & Facilitating Change | **104.25 Hz** | $417 / 4$ |
| **2** | **Sacral Plexus** | L1 - L5 Lumbar | **396 Hz** | Liberating Guilt, Fear & Emotional Blocks | **99.00 Hz** | $396 / 4$ |
| **1** | **Sacrum / Root Tail** | S1 - S4 Sacral | **174 Hz** | Foundation, Pain Reliever & Deep Stress Relief | **174.00 Hz** | **Direct 1:1 Match!** |

---

## 3. Core Presets & Therapy Protocols

### Preset 1: "The 7-Chakra Spinal Cascade" (14 Minutes)
*   **Description:** A progressive ascending journey up the spine (*Sushumna Nadi*).
*   **Sequence:** 
    *   00:00 - 02:00 $\rightarrow$ Node 1 (174 Hz) — Root activation
    *   02:00 - 04:00 $\rightarrow$ Node 2 (396 Hz) — Sacral unblocking
    *   04:00 - 06:00 $\rightarrow$ Node 3 (417 Hz) — Solar transformation
    *   06:00 - 08:00 $\rightarrow$ Node 4 (432 Hz) — Mid-thoracic alignment
    *   08:00 - 10:00 $\rightarrow$ Node 5 (528 Hz) — Heart expansion
    *   10:00 - 12:00 $\rightarrow$ Node 6 (741 Hz) — Throat & cervical clarity
    *   12:00 - 14:00 $\rightarrow$ Node 7 (963 Hz) — Suboccipital crown resonance

### Preset 2: "Somatic Pain Relief & Deep Grounding" (20 Minutes)
*   **Target Areas:** Nodes 1, 2, and 3 (Lower Spine & Sacral Tail).
*   **Frequencies:** Locked at **174 Hz** (direct 1:1) and **396 Hz** ($99 \text{ Hz}$ sub-octave).
*   **Mechanism:** Activates Gate Control Theory of Pain to block nociceptive pain signals along the lumbar and sacral paraspinal nerves.

### Preset 3: "Vagal Awakening & High Clarity" (15 Minutes)
*   **Target Areas:** Nodes 5, 6, and 7 (Heart Center & Suboccipital Neck Collar).
*   **Frequencies:** Synchronized **528 Hz**, **741 Hz**, and **963 Hz** tones with corresponding sub-octave haptic swelling waveforms.
*   **Mechanism:** Direct vagal down-regulation via bone conduction at the occipital ridge and pharyngeal plexus stimulation.

---

## 4. Hardware & Software Implementation Parameters

```json
{
  "preset_id": "chakra_cascade_v1",
  "name": "The 7-Chakra Spinal Cascade",
  "duration_seconds": 840,
  "nodes": [
    { "node_id": 1, "name": "Sacrum", "audio_hz": 174.0, "haptic_hz": 174.0, "waveform": "sine_undulate" },
    { "node_id": 2, "name": "Sacral", "audio_hz": 396.0, "haptic_hz": 99.0, "waveform": "pulse_swell" },
    { "node_id": 3, "name": "Solar", "audio_hz": 417.0, "haptic_hz": 104.25, "waveform": "pulse_swell" },
    { "node_id": 4, "name": "Mid_Thoracic", "audio_hz": 432.0, "haptic_hz": 108.0, "waveform": "sine_undulate" },
    { "node_id": 5, "name": "Heart", "audio_hz": 528.0, "haptic_hz": 132.0, "waveform": "sine_undulate" },
    { "node_id": 6, "name": "Cervical", "audio_hz": 741.0, "haptic_hz": 92.63, "waveform": "micro_flutter" },
    { "node_id": 7, "name": "Suboccipital", "audio_hz": 963.0, "haptic_hz": 120.38, "waveform": "micro_flutter" }
  ]
}
```
