# 🌶️ SPICE — The AI-Powered Couples Intimacy Engine
## Master System Blueprint & Launch Strategy

> **Project Goal:** Build a sleek, dark-mode, AI-driven couples date-night game that matches partners' hidden boundaries and generates customized, gamified dares, scenarios, and intimacy prompts in real-time.
> **Target Platforms:** iOS (Apple App Store) & Android (Google Play Store) via React Native (Expo).
> **Primary Build Engine:** Designed for automated full-stack build execution via Claude Code.

---

## 🚀 Tomorrow Night's Roadmap (Feature Queue)

### 1. 🖼️ 1:1 Dynamic Image-to-Act Mapping Engine
* **Goal:** Ensure every generated card artwork dynamically matches the exact physical position, dare, or act recommended on the card.
* **Implementation:** Expand pose categories (`massage`, `kiss`, `lotus`, `elevated_arch`, `blindfold`, `spanking`, `embraced`) with a dedicated neon silhouette asset matrix & dynamic image generator pipeline.

### 2. 🎵 Ambient Music & Rhythmic Soundscape Engine (Wave Persona Integration)
* **Goal:** Synchronize background audio soundscapes to match the exact pace, rhythm, and intensity of the active card prompt.
* **Features:**
  * Level 1 (Teasing) $\rightarrow$ 432 Hz Warm ambient acoustic swells.
  * Level 2 (Intimate Touch) $\rightarrow$ 528 Hz Solfeggio heart resonance & slow breath pacing audio.
  * Level 3 (Daring Sex Stuff) $\rightarrow$ Deep rhythmic pulse beats matching target movement tempos.
  * Level 4 (Kink & Power) $\rightarrow$ Low-frequency bass hums & dramatic sensory audio cues.

---

## 1. Executive Summary & Brand Positioning

### Brand Identity
* **App Name:** SPICE — Couples Date Night Game & Intimacy Companion
* **Target Audience:** Couples looking to break routine, enhance communication, and explore new levels of intimacy.
* **Core Value Proposition:** Eliminates awkwardness with a "Secret Intersection" matching system. Neither partner sees raw survey answers—the game *only* generates activities where both secretly opted in!

---

## 2. Core Feature Set & User Flow

```
[ Launch App ] 
      │
      ├──> [ Select Game Mode ] (Pass & Play vs Realtime Sync)
      ├──> [ Secret Boundary Calibration ] (25 Topics rated 1-3)
      ├──> [ AI "Secret Intersection" Calculation ]
      ├──> [ Select Intensity Level & Heat ]
      │         ├── 💋 Level 1: Teasing (Flirting, stripping rules, eye lock)
      │         ├── 🤲 Level 2: Intimate Touching (Massage, erogenous focus, blindfolds)
      │         ├── 🔥 Level 3: Daring Sex Stuff (Explicit positions, intercourse dares)
      │         └── ⚡ Level 4: Kink & Fantasy (Restraints, spanking, Sub/Dom dynamics)
      │
      └──> [ Dynamic 8-Card AI Game Loop + Rhythmic Music Sync ]
```

---

## 3. Technology Stack & Architecture

| Component | Tech Selected | Rationale |
| :--- | :--- | :--- |
| **Mobile Framework** | **React Native + Expo (SDK 51+)** | Write once, deploy natively to iOS (.ipa) and Android (.aab). |
| **Styling** | **NativeWind (Tailwind CSS)** | Sleek dark-mode utilities. |
| **Backend / DB** | **Supabase (Postgres & Realtime)** | Ephemeral session pairing & WebSockets. |
| **AI Engine** | **OpenAI API (`gpt-4o-mini`)** | Sub-second response times, structured JSON outputs. |
| **Audio Engine** | **Expo Audio / Web Audio API** | Dynamic Solfeggio tones & rhythmic soundscapes. |
