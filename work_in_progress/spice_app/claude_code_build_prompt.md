# ⚡ Claude Code Execution Master Prompt — SPICE App Build

> **How to use this file:** Open Claude Code inside the `work_in_progress/spice_app/` directory and feed it the step-by-step instructions below to build the mobile app repository.

---

## 🎯 Master Instruction to Claude Code

```text
You are an expert React Native, Expo, and Supabase full-stack engineer. 
Your task is to build the complete codebase for "SPICE", a dark-mode couples date-night game app built with React Native (Expo SDK 51), NativeWind (Tailwind CSS), Supabase, and OpenAI API (gpt-4o-mini).

Follow the modular phases below step by step. Write clean, production-grade TypeScript code with zero placeholder stubbing.
```

---

## 📦 PHASE 1: Project Initialization

Execute shell commands to scaffold the Expo project:

```bash
npx create-expo-app@latest code --template blank-typescript
cd code
npx expo install react-native-reanimated react-native-gesture-handler react-native-screens react-native-safe-area-context expo-status-bar expo-linear-gradient expo-haptics @supabase/supabase-js @react-navigation/native @react-navigation/native-stack
npm install nativewind tailwindcss react-native-svg lucide-react-native openai
```

---

## 🗄️ PHASE 2: Supabase Database Schema

Create `code/supabase/schema.sql`:

```sql
-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Sessions Table for Dual-Phone Sync
create table if not exists public.game_sessions (
  id uuid primary key default uuid_generate_v4(),
  room_code varchar(6) unique not null,
  mode varchar(20) not null default 'pass_and_play', -- 'pass_and_play' or 'realtime_sync'
  status varchar(20) not null default 'calibrating', -- 'calibrating', 'playing', 'finished'
  partner_1_survey jsonb default '{}'::jsonb,
  partner_2_survey jsonb default '{}'::jsonb,
  allowed_categories jsonb default '[]'::jsonb,
  current_deck jsonb default '[]'::jsonb,
  current_card_index int default 0,
  created_at timestamp with time zone default now()
);

-- Enable Realtime on game_sessions
alter publication supabase_realtime add table public.game_sessions;
```

---

## 🤖 PHASE 3: OpenAI AI Scenario Generation Engine

Create `code/src/services/aiScenarioEngine.ts`:

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.EXPO_PUBLIC_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true, // Used for local Expo app execution
});

export interface CardScenario {
  id: string;
  type: 'dare' | 'truth' | 'scenario' | 'roleplay';
  intensity_level: 1 | 2 | 3 | 4;
  title: string;
  description: string;
  action_prompt: string;
  timer_seconds?: number;
  category: string;
}

export async function generateDeck(
  allowedCategories: string[],
  intensityLevel: number,
  partnerNames: { p1: string; p2: string }
): Promise<CardScenario[]> {
  const systemPrompt = `You are the AI Scenario Director for "SPICE", a couples intimacy game.
Your task is to generate a custom 10-card deck of romantic, sensual, fun, and intimate prompts for two partners: ${partnerNames.p1} and ${partnerNames.p2}.

RULES:
1. STRICT BOUNDARIES: You must ONLY generate cards belonging to these approved categories: ${JSON.stringify(allowedCategories)}.
2. INTENSITY LEVEL: ${intensityLevel} out of 4.
   - Level 1: Lighthearted, flirty, eye contact, verbal compliments, light touch.
   - Level 2: Sensual, heating up, massage, sensory deprivation (blindfold/ice), teasing.
   - Level 3: Adventurous, spicy dares, roleplay scenarios, physical intimacy escalation.
   - Level 4: Deep vulnerability, emotional intimacy, intense eye-gazing, deep connection questions.
3. FORMAT: Return exclusively valid JSON matching the specified JSON Schema array of 10 card objects.
4. Tone: Elegant, playful, consensual, exciting, respectful, high-vibe.`;

  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: `Generate 10 unique game cards for level ${intensityLevel}.` },
    ],
    response_format: { type: 'json_object' },
    temperature: 0.8,
  });

  const data = JSON.parse(response.choices[0].message.content || '{}');
  return data.cards || [];
}
```

---

## 📱 PHASE 4: Core UI Screens to Build

Claude Code will construct the following screens inside `code/src/screens/`:

1. **`HomeScreen.tsx`**
   * Dark plum/burgundy linear gradient (`LinearGradient`).
   * Sleek glowing logo, "Start New Date Night" button, "Enter Room Code" input.
   * Mode toggle: *Pass & Play* vs *Dual Phone Sync*.

2. **`BoundarySurveyScreen.tsx`**
   * Fast swipe/tap cards for 25 topics (e.g. *Massage & Touch*, *Sensory Deprivation*, *Roleplay*, *Vulnerability & Q&A*, *Outdoor Adventure*, etc.).
   * 3 Buttons per card: 🟢 Hell Yes / 🟡 Curious / 🔴 Pass.
   * Haptic feedback on tap (`expo-haptics`).

3. **`GameDeckScreen.tsx`**
   * Swipable card carousel (React Native Reanimated).
   * Timer overlay for timed dares (e.g. "2-minute sensory massage").
   * "Complete Dare", "Skip / Re-roll", and "Escalate Intensity" controls.

---

## 🎨 Design System Guide for Claude Code

* **Background:** Deep Plum / Onyx Noir (`#0F0814`, `#1A0C27`, `#28113B`)
* **Accents:** Neon Rose (`#FF2E63`), Amber Glow (`#FF9F43`), Emerald Safe (`#10B981`)
* **Typography:** Clean sans-serif, bold tracking, sensual rounded cards with glassmorphism blur borders.
