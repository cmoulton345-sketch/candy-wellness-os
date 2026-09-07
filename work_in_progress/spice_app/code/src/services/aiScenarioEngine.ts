import OpenAI from 'openai';
import { CardScenario, IntensityLevel, Rating } from '../types';

export function calculateSecretIntersection(
  p1Survey: Record<string, Rating>,
  p2Survey: Record<string, Rating>
): string[] {
  const allowedCategories: string[] = [];
  const allCategoryIds = Array.from(new Set([...Object.keys(p1Survey), ...Object.keys(p2Survey)]));

  for (const catId of allCategoryIds) {
    const r1 = p1Survey[catId];
    const r2 = p2Survey[catId];

    if (r1 === 'red' || r2 === 'red') {
      continue;
    }

    if ((r1 === 'green' || r1 === 'yellow') && (r2 === 'green' || r2 === 'yellow')) {
      allowedCategories.push(catId);
    }
  }

  return allowedCategories;
}

export async function generateDeck(
  allowedCategories: string[],
  intensityLevel: IntensityLevel,
  partnerNames: { p1: string; p2: string }
): Promise<CardScenario[]> {
  const geminiKey = process.env.EXPO_PUBLIC_GEMINI_API_KEY;
  const openaiKey = process.env.EXPO_PUBLIC_OPENAI_API_KEY;
  const openrouterKey = process.env.EXPO_PUBLIC_OPENROUTER_API_KEY || process.env.OPENROUTER_API_KEY;

  const categoriesToUse = allowedCategories.length > 0
    ? allowedCategories
    : ['teasing_flirt', 'intimate_touch', 'daring_positions', 'vulnerability_truth'];

  const systemPrompt = `You are the AI Intimacy & Date Night Director for "SPICE", an uncensored couples game.
Generate a custom 8-CARD GAME DECK for partners: ${partnerNames.p1} and ${partnerNames.p2}.

RECALIBRATED INTENSITY LEVELS:
- LEVEL 1 (Teasing): Flirting, light touch, stripping rules, eye lock.
- LEVEL 2 (Intimate Touching): Slow massage, erogenous zone exploration, oral focus, sensory blindfolds.
- LEVEL 3 (Daring Sex Stuff): Explicit physical positions, physical intercourse dares, climax pacing.
- LEVEL 4 (Kink & Power Dynamics): Sub/Dom dynamics, restraints, spanking, wax/ice play, advanced roleplay.

RULES:
1. ONLY use approved categories: ${JSON.stringify(categoriesToUse)}.
2. Provide 8 UNIQUE, DISTINCT cards progressing naturally from warm-up (Card 1) to peak climax (Card 8).
3. EVERY CARD MUST HAVE A UNIQUE TITLE AND UNIQUE ACTION DARE PROMPT.
4. Include "stick_figure_pose" field matching EXACTLY one of: "blindfold" | "spanking" | "massage" | "kiss" | "lotus" | "kink_bondage" | "strip_tease" | "temperature_play" | "roleplay_fantasy" | "wild_position" | "sensual_pose". Ensure each of the 8 cards has a DIFFERENT pose!

JSON OUTPUT SCHEMA:
{
  "cards": [
    {
      "id": "card-1",
      "type": "dare" | "truth" | "position" | "roleplay",
      "intensity_level": ${intensityLevel},
      "title": "Unique Bold Title",
      "description": "Sensual scenario context",
      "action_prompt": "Explicit, clear, exciting step-by-step instruction for the active turn taker",
      "timer_seconds": 120,
      "category": "category_id",
      "stick_figure_pose": "kink_bondage"
    }
  ]
}`;

  // 1. TRY OPENROUTER (ROUTED TO GOOGLE GEMINI FLASH)
  if (openrouterKey && openrouterKey.trim().length > 0) {
    try {
      const openai = new OpenAI({
        baseURL: 'https://openrouter.ai/api/v1',
        apiKey: openrouterKey,
        dangerouslyAllowBrowser: true,
        defaultHeaders: {
          'HTTP-Referer': 'https://spice-app.internal',
          'X-Title': 'SPICE App',
        },
      });

      const response = await openai.chat.completions.create({
        model: 'google/gemini-2.5-flash',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: `Generate a high-energy 8-card deck for Level ${intensityLevel}.` },
        ],
        response_format: { type: 'json_object' },
        temperature: 0.85,
      });

      const parsed = JSON.parse(response.choices[0].message.content || '{}');
      if (parsed.cards && parsed.cards.length >= 8) {
        return parsed.cards;
      }
    } catch (error) {
      console.error('OpenRouter Gemini Generation Error, trying direct APIs:', error);
    }
  }

  // 2. TRY DIRECT GOOGLE GEMINI API
  if (geminiKey && geminiKey.trim().length > 0) {
    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${geminiKey}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [
              {
                role: 'user',
                parts: [{ text: `${systemPrompt}\n\nTask: Generate a high-energy 8-card deck for Level ${intensityLevel}.` }],
              },
            ],
            generationConfig: {
              responseMimeType: 'application/json',
              temperature: 0.85,
            },
          }),
        }
      );

      const json = await response.json();
      const rawText = json?.candidates?.[0]?.content?.parts?.[0]?.text;
      if (rawText) {
        const parsed = JSON.parse(rawText);
        if (parsed.cards && parsed.cards.length >= 8) {
          return parsed.cards;
        }
      }
    } catch (error) {
      console.error('Gemini 2.5 Flash Generation Error, trying OpenAI/fallback:', error);
    }
  }

  // 2. TRY OPENAI (FALLBACK)
  if (openaiKey && openaiKey.trim().length > 0) {
    try {
      const openai = new OpenAI({
        apiKey: openaiKey,
        dangerouslyAllowBrowser: true,
      });

      const response = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: `Generate an 8-card deck for Level ${intensityLevel}.` },
        ],
        response_format: { type: 'json_object' },
        temperature: 0.85,
      });

      const parsed = JSON.parse(response.choices[0].message.content || '{}');
      if (parsed.cards && parsed.cards.length >= 8) {
        return parsed.cards;
      }
    } catch (error) {
      console.error('OpenAI Generation Error, falling back to local master deck:', error);
    }
  }

  // 3. MASTER LOCAL FALLBACK DECK
  return getFallbackDeck(intensityLevel);
}

function getFallbackDeck(level: IntensityLevel): CardScenario[] {
  if (level === 4) {
    return [
      {
        id: 'lvl4-1',
        type: 'dare',
        intensity_level: 4,
        title: 'Silk Restraints & Surrender',
        description: 'Establish the power dynamic for the evening.',
        action_prompt: 'Gently tie your partner’s wrists using silk scarves or soft ties to the headboard or chair. They must remain completely still until released.',
        timer_seconds: 120,
        category: 'kink_power',
        stick_figure_pose: 'kink_bondage',
      },
      {
        id: 'lvl4-2',
        type: 'dare',
        intensity_level: 4,
        title: 'Sensory Temperature Contrast',
        description: 'Combine ice shocks with deep thermal warmth.',
        action_prompt: 'Trace an ice cube down your partner’s throat, stomach, and inner thighs, followed immediately by warm breath and lingering kisses.',
        timer_seconds: 180,
        category: 'sensory_deprivation',
        stick_figure_pose: 'blindfold',
      },
      {
        id: 'lvl4-3',
        type: 'dare',
        intensity_level: 4,
        title: 'The Discipline Command',
        description: 'Pacing control and physical feedback.',
        action_prompt: 'Deliver 10 firm, rhythmic spanks to your partner’s hips. Your partner must thank you aloud after each one.',
        timer_seconds: 90,
        category: 'kink_power',
        stick_figure_pose: 'kink_bondage',
      },
      {
        id: 'lvl4-4',
        type: 'roleplay',
        intensity_level: 4,
        title: 'Stranger in a Dark Lounge',
        description: 'Immersive alter-ego fantasy game.',
        action_prompt: 'Assume new alter-ego names. Partner A is an elite collector; Partner B is a mysterious stranger who must negotiate a taboo reward.',
        category: 'fantasy_roleplay',
        stick_figure_pose: 'sensual_pose',
      },
      {
        id: 'lvl4-5',
        type: 'position',
        intensity_level: 4,
        title: 'Bound Submission Position',
        description: 'Restrained elevated contact.',
        action_prompt: 'With Partner B’s hands bound behind their back, Partner A takes full control of the pace and depth.',
        timer_seconds: 240,
        category: 'daring_positions',
        stick_figure_pose: 'wild_position',
      },
      {
        id: 'lvl4-6',
        type: 'dare',
        intensity_level: 4,
        title: 'Extreme Edging & Command',
        description: 'Denial and intense climax buildup.',
        action_prompt: 'Bring your partner to the absolute brink of release three separate times, forcing them to beg for permission before allowing completion.',
        timer_seconds: 300,
        category: 'kink_power',
        stick_figure_pose: 'kink_bondage',
      },
      {
        id: 'lvl4-7',
        type: 'truth',
        intensity_level: 4,
        title: 'Forbidden Fantasy Secret',
        description: 'Unfiltered confession.',
        action_prompt: 'Share one taboo kink or secret fantasy you have never admitted out loud to anyone.',
        category: 'vulnerability_truth',
        stick_figure_pose: 'embraced',
      },
      {
        id: 'lvl4-8',
        type: 'position',
        intensity_level: 4,
        title: 'Total Release & Surrender',
        description: 'The peak climax of the kink session.',
        action_prompt: 'Release all restraints and unite in a passionate, intense climax matching every breath.',
        timer_seconds: 300,
        category: 'daring_positions',
        stick_figure_pose: 'embraced',
      },
    ];
  }

  if (level === 3) {
    return [
      {
        id: 'lvl3-1',
        type: 'dare',
        intensity_level: 3,
        title: 'Sensual Undressing',
        description: 'Remove clothing using only your teeth.',
        action_prompt: 'Slowly unbutton or peel off your partner’s shirt using only your lips and teeth. No hands allowed.',
        timer_seconds: 90,
        category: 'teasing_flirt',
        stick_figure_pose: 'sensual_pose',
      },
      {
        id: 'lvl3-2',
        type: 'dare',
        intensity_level: 3,
        title: 'Erogenous Zone Mapping',
        description: 'Kiss everywhere except the lips.',
        action_prompt: 'Focus intensely on the inner thighs, neck, and pelvic ridge. No kissing on the mouth until the 2-minute timer ends.',
        timer_seconds: 120,
        category: 'intimate_touch',
        stick_figure_pose: 'kiss',
      },
      {
        id: 'lvl3-3',
        type: 'position',
        intensity_level: 3,
        title: 'The Deep Lotus',
        description: 'Seated face-to-face contact.',
        action_prompt: 'Partner A sits cross-legged. Partner B wraps their legs around Partner A’s waist, locking eyes and moving slowly together.',
        timer_seconds: 180,
        category: 'daring_positions',
        stick_figure_pose: 'wild_position',
      },
      {
        id: 'lvl3-4',
        type: 'dare',
        intensity_level: 3,
        title: 'Oral Tease & Control',
        description: 'Intense oral focus with speed commands.',
        action_prompt: 'Deliver 3 minutes of intense oral focus. Partner A controls Partner B’s rhythm by tapping their shoulder once for slow, twice for fast.',
        timer_seconds: 180,
        category: 'intimate_touch',
        stick_figure_pose: 'embraced',
      },
      {
        id: 'lvl3-5',
        type: 'position',
        intensity_level: 3,
        title: 'The Elevated Arch',
        description: 'Maximum depth using pillows.',
        action_prompt: 'Place two firm pillows beneath Partner B’s hips to elevate the pelvis for deep, rhythmic contact.',
        timer_seconds: 240,
        category: 'daring_positions',
        stick_figure_pose: 'wild_position',
      },
      {
        id: 'lvl3-6',
        type: 'dare',
        intensity_level: 3,
        title: 'The 30-Second Pause',
        description: 'Teasing control at maximum tension.',
        action_prompt: 'Build the intensity to a climax threshold, then stop all movement completely for 30 seconds while looking into each other’s eyes.',
        timer_seconds: 180,
        category: 'daring_positions',
        stick_figure_pose: 'wild_position',
      },
      {
        id: 'lvl3-7',
        type: 'truth',
        intensity_level: 3,
        title: 'Erotic Confession',
        description: 'Vivid detailed fantasy sharing.',
        action_prompt: 'Describe in vivid detail the exact position or scenario you want to try next.',
        category: 'vulnerability_truth',
        stick_figure_pose: 'sensual_pose',
      },
      {
        id: 'lvl3-8',
        type: 'position',
        intensity_level: 3,
        title: 'Synchronized Climax',
        description: 'Final escalation of the date night.',
        action_prompt: 'Match your breath and rhythm together until both partners reach full release.',
        timer_seconds: 300,
        category: 'daring_positions',
        stick_figure_pose: 'embraced',
      },
    ];
  }

  if (level === 2) {
    return [
      {
        id: 'lvl2-1',
        type: 'dare',
        intensity_level: 2,
        title: 'Sensual Oil Massage',
        description: 'Warming shoulder and neck touch.',
        action_prompt: 'Apply warming lotion or massage oil to your partner’s shoulders and neck, pressing deeply into tension spots for 2 minutes.',
        timer_seconds: 120,
        category: 'intimate_touch',
        stick_figure_pose: 'massage',
      },
      {
        id: 'lvl2-2',
        type: 'dare',
        intensity_level: 2,
        title: 'Blindfold Whispers',
        description: 'Sensory enhancement with blindfold.',
        action_prompt: 'Blindfold your partner and whisper 3 suggestive desires into their ear while gently tracing your fingernails along their arms.',
        timer_seconds: 90,
        category: 'sensory_deprivation',
        stick_figure_pose: 'blindfold',
      },
      {
        id: 'lvl2-3',
        type: 'dare',
        intensity_level: 2,
        title: 'Inner Thigh Trace',
        description: 'Teasing erogenous zones.',
        action_prompt: 'Use slow, feather-light fingertips to trace small circles along your partner’s inner thighs without touching their center.',
        timer_seconds: 120,
        category: 'intimate_touch',
        stick_figure_pose: 'sensual_pose',
      },
      {
        id: 'lvl2-4',
        type: 'dare',
        intensity_level: 2,
        title: 'Slow Motion Kissing',
        description: 'Uninterrupted lip contact.',
        action_prompt: 'Kiss your partner in ultra-slow motion for 90 seconds without separating your lips once.',
        timer_seconds: 90,
        category: 'teasing_flirt',
        stick_figure_pose: 'kiss',
      },
      {
        id: 'lvl2-5',
        type: 'truth',
        intensity_level: 2,
        title: 'Sensual Memory',
        description: 'Recalling peak romantic moments.',
        action_prompt: 'Tell your partner about the exact moment you felt the strongest physical spark with them.',
        category: 'vulnerability_truth',
        stick_figure_pose: 'embraced',
      },
      {
        id: 'lvl2-6',
        type: 'dare',
        intensity_level: 2,
        title: 'Heartbeat Pacing',
        description: 'Synchronized chest press.',
        action_prompt: 'Lie chest-to-chest with no shirt on. Synchronize your breathing until both your hearts beat together.',
        timer_seconds: 120,
        category: 'intimate_touch',
        stick_figure_pose: 'embraced',
      },
      {
        id: 'lvl2-7',
        type: 'dare',
        intensity_level: 2,
        title: 'Ice Cube Trace',
        description: 'Cool sensory temperature contrast.',
        action_prompt: 'Trace an ice cube down your partner’s spine, then follow it instantly with warm kisses.',
        timer_seconds: 90,
        category: 'sensory_deprivation',
        stick_figure_pose: 'massage',
      },
      {
        id: 'lvl2-8',
        type: 'position',
        intensity_level: 2,
        title: 'The Reclined Embrace',
        description: 'Final relaxation position.',
        action_prompt: 'Hold your partner tight in a full-body recline, enjoying the warmth and affection.',
        category: 'intimate_touch',
        stick_figure_pose: 'embraced',
      },
    ];
  }

  // Level 1: Teasing
  return [
    {
      id: 'lvl1-1',
      type: 'dare',
      intensity_level: 1,
      title: '60-Second Eye Lock',
      description: 'Intense eye contact game.',
      action_prompt: 'Look into each other’s eyes for 60 seconds without speaking. First one to blink or laugh gives the other a 30-second neck rub.',
      timer_seconds: 60,
      category: 'teasing_flirt',
      stick_figure_pose: 'sensual_pose',
    },
    {
      id: 'lvl1-2',
      type: 'truth',
      intensity_level: 1,
      title: 'Attraction Confession',
      description: 'Flirty compliment.',
      action_prompt: 'Tell your partner what physical feature of theirs caught your attention first today.',
      category: 'teasing_flirt',
      stick_figure_pose: 'kiss',
    },
    {
      id: 'lvl1-3',
      type: 'dare',
      intensity_level: 1,
      title: 'Finger Trace Spelling',
      description: 'Tactile back guessing game.',
      action_prompt: 'Trace a secret flirtatious word on your partner’s back with your fingertip. They must guess what word you spelled.',
      timer_seconds: 60,
      category: 'teasing_flirt',
      stick_figure_pose: 'massage',
    },
    {
      id: 'lvl1-4',
      type: 'dare',
      intensity_level: 1,
      title: 'Whispered Secret',
      description: 'Earside tease.',
      action_prompt: 'Whisper one thing you love about your partner into their ear in your softest, most sensual voice.',
      category: 'teasing_flirt',
      stick_figure_pose: 'embraced',
    },
    {
      id: 'lvl1-5',
      type: 'truth',
      intensity_level: 1,
      title: 'Dream Date Night',
      description: 'Future romantic planning.',
      action_prompt: 'If you could fly anywhere in the world tonight for a secret getaway, where would you take your partner?',
      category: 'vulnerability_truth',
      stick_figure_pose: 'sensual_pose',
    },
    {
      id: 'lvl1-6',
      type: 'dare',
      intensity_level: 1,
      title: 'Hand Massage',
      description: 'Gentle hand touch.',
      action_prompt: 'Interlock fingers and give your partner a slow 1-minute palm and hand massage.',
      timer_seconds: 60,
      category: 'teasing_flirt',
      stick_figure_pose: 'embraced',
    },
    {
      id: 'lvl1-7',
      type: 'dare',
      intensity_level: 1,
      title: 'Butterfly Kisses',
      description: 'Eyelash cheek caress.',
      action_prompt: 'Flutter your eyelashes gently against your partner’s cheek until they laugh or smile.',
      category: 'teasing_flirt',
      stick_figure_pose: 'kiss',
    },
    {
      id: 'lvl1-8',
      type: 'dare',
      intensity_level: 1,
      title: 'The Warm Hug',
      description: '30-second embrace.',
      action_prompt: 'Hold your partner in a tight, warm 30-second embrace, resting your chin on their shoulder.',
      timer_seconds: 30,
      category: 'teasing_flirt',
      stick_figure_pose: 'embraced',
    },
  ];
}
