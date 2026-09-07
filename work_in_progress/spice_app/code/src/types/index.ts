export type IntensityLevel = 1 | 2 | 3 | 4;

export type GameMode = 'pass_and_play' | 'realtime_sync';

export type Rating = 'green' | 'yellow' | 'red';

export interface IntimacyCategory {
  id: string;
  title: string;
  description: string;
  icon: string;
}

export interface CardScenario {
  id: string;
  type: 'dare' | 'truth' | 'scenario' | 'roleplay' | 'position';
  intensity_level: IntensityLevel;
  title: string;
  description: string;
  action_prompt: string;
  timer_seconds?: number;
  category: string;
  stick_figure_pose?: 'massage' | 'kiss' | 'blindfold' | 'embraced' | 'sensual_pose' | 'wild_position' | 'kink_bondage';
}

export interface GameSession {
  id: string;
  room_code: string;
  mode: GameMode;
  status: 'calibrating' | 'playing' | 'finished';
  partner_1_name: string;
  partner_2_name: string;
  partner_1_survey: Record<string, Rating>;
  partner_2_survey: Record<string, Rating>;
  allowed_categories: string[];
  current_deck: CardScenario[];
  current_card_index: number;
}

export const CATEGORIES: IntimacyCategory[] = [
  { id: 'teasing_flirt', title: 'Teasing & Flirting', description: 'Suggestive compliments, clothing removal rules, slow anticipation.', icon: 'sparkles' },
  { id: 'intimate_touch', title: 'Intimate Touch & Erogenous Zones', description: 'Targeted erogenous touch, oral focus, sensory oils, slow massage.', icon: 'hand' },
  { id: 'sensory_deprivation', title: 'Blindfolds & Sensory Play', description: 'Ice, warmth, silk restraints, blindfolds, heightened anticipation.', icon: 'eye-off' },
  { id: 'daring_positions', title: 'Daring Positions & Sex Dares', description: 'Explicit positions, passionate escalation, physical intensity.', icon: 'flame' },
  { id: 'fantasy_roleplay', title: 'Roleplay & Alter-Egos', description: 'Secret characters, stranger-in-a-bar scenarios, taboos.', icon: 'mask' },
  { id: 'kink_power', title: 'Kink & Power Dynamics', description: 'Light dominance/submission, spanking, restraints, wax play.', icon: 'zap' },
  { id: 'vulnerability_truth', title: 'Deep Vulnerability & Desires', description: 'Unspoken fantasies, secret confessions, erotic truths.', icon: 'heart' },
];
