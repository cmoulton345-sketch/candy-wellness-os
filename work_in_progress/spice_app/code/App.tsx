import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  TextInput,
  ScrollView,
  SafeAreaView,
  StatusBar,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import { CATEGORIES, CardScenario, IntensityLevel, Rating } from './src/types';
import { calculateSecretIntersection, generateDeck } from './src/services/aiScenarioEngine';
import { NeonSilhouette } from './src/components/NeonSilhouette';
import { soundscapeEngine, MoodGenre } from './src/services/soundscapeEngine';

type ScreenState = 'welcome' | 'survey_p1' | 'survey_p2' | 'deck';

export default function App() {
  const [screen, setScreen] = useState<ScreenState>('welcome');
  const [partner1, setPartner1] = useState('Alex');
  const [partner2, setPartner2] = useState('Sam');
  const [intensity, setIntensity] = useState<IntensityLevel>(3);

  const [p1Survey, setP1Survey] = useState<Record<string, Rating>>({});
  const [p2Survey, setP2Survey] = useState<Record<string, Rating>>({});

  const [allowedCategories, setAllowedCategories] = useState<string[]>([]);
  const [deck, setDeck] = useState<CardScenario[]>([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const [timerSeconds, setTimerSeconds] = useState<number | null>(null);
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [activeMood, setActiveMood] = useState<MoodGenre>('sensual_rnb');
  const [customAudioUrl, setCustomAudioUrl] = useState('');
  const [showMusicInput, setShowMusicInput] = useState(false);

  useEffect(() => {
    let interval: any = null;
    if (isTimerRunning && timerSeconds !== null && timerSeconds > 0) {
      interval = setInterval(() => {
        setTimerSeconds((prev) => (prev !== null && prev > 0 ? prev - 1 : 0));
      }, 1000);
    } else if (timerSeconds === 0) {
      setIsTimerRunning(false);
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, timerSeconds]);

  useEffect(() => {
    if (screen === 'deck') {
      soundscapeEngine.playForIntensity(intensity);
    } else {
      soundscapeEngine.stop();
    }
    return () => {
      soundscapeEngine.stop();
    };
  }, [screen, intensity]);

  const toggleAudioMute = () => {
    const nextMuted = !isMuted;
    setIsMuted(nextMuted);
    soundscapeEngine.setMuted(nextMuted);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const handleSelectMood = (genre: MoodGenre) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setActiveMood(genre);
    if (genre === 'custom') {
      setShowMusicInput(true);
    } else {
      setShowMusicInput(false);
      soundscapeEngine.setMoodGenre(genre);
    }
  };

  const applyCustomAudioUrl = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    soundscapeEngine.setMoodGenre('custom', customAudioUrl);
    setShowMusicInput(false);
  };


  const handleStartSurvey = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setScreen('survey_p1');
  };

  const handleRating = (catId: string, rating: Rating, partner: 1 | 2) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    if (partner === 1) {
      setP1Survey((prev) => ({ ...prev, [catId]: rating }));
    } else {
      setP2Survey((prev) => ({ ...prev, [catId]: rating }));
    }
  };

  const finishP1Survey = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setScreen('survey_p2');
  };

  const finishP2SurveyAndGenerate = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    setIsLoading(true);

    const allowed = calculateSecretIntersection(p1Survey, p2Survey);
    setAllowedCategories(allowed);

    const cards = await generateDeck(allowed, intensity, { p1: partner1, p2: partner2 });
    setDeck(cards);
    setCurrentCardIndex(0);
    setIsLoading(false);
    setScreen('deck');
  };

  const reRollDeck = async (targetIntensity?: IntensityLevel) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    setIsLoading(true);
    const lvlToUse = targetIntensity || intensity;
    const cards = await generateDeck(allowedCategories, lvlToUse, { p1: partner1, p2: partner2 });
    setDeck(cards);
    setCurrentCardIndex(0);
    setIsLoading(false);
  };

  const escalateHeat = async () => {
    const nextLvl = (intensity < 4 ? (intensity + 1) : 1) as IntensityLevel;
    setIntensity(nextLvl);
    await reRollDeck(nextLvl);
  };

  const nextCard = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setIsTimerRunning(false);
    setTimerSeconds(null);
    if (currentCardIndex < deck.length - 1) {
      setCurrentCardIndex((prev) => prev + 1);
    } else {
      alert('🔥 Session Complete! You completed all 8 intimate dares.');
    }
  };

  const startTimer = (seconds: number) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    setTimerSeconds(seconds);
    setIsTimerRunning(true);
  };

  const activeCard = deck[currentCardIndex];

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <LinearGradient colors={['#0F0814', '#1A0C27', '#28113B']} style={styles.gradient}>
        
        {/* WELCOME SCREEN */}
        {screen === 'welcome' && (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={styles.headerBox}>
              <Text style={styles.brandTitle}>🌶️ SPICE</Text>
              <Text style={styles.brandSub}>Couples Date Night & Intimacy Engine</Text>
            </View>

            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Partner Names</Text>
              <Text style={styles.label}>Partner 1</Text>
              <TextInput
                style={styles.input}
                value={partner1}
                onChangeText={setPartner1}
                placeholderTextColor="#7E6B8F"
              />
              <Text style={styles.label}>Partner 2</Text>
              <TextInput
                style={styles.input}
                value={partner2}
                onChangeText={setPartner2}
                placeholderTextColor="#7E6B8F"
              />
            </View>

            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Select Heat Level (1 to 4)</Text>
              <View style={styles.intensityRow}>
                {([1, 2, 3, 4] as IntensityLevel[]).map((lvl) => (
                  <TouchableOpacity
                    key={lvl}
                    style={[styles.lvlBtn, intensity === lvl && styles.lvlBtnActive]}
                    onPress={() => {
                      Haptics.selectionAsync();
                      setIntensity(lvl);
                    }}
                  >
                    <Text style={[styles.lvlText, intensity === lvl && styles.lvlTextActive]}>
                      Lvl {lvl}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>

              <Text style={styles.intensityDesc}>
                {intensity === 1 && '💋 Level 1: Teasing (Suggestive flirting, stripping rules, eye lock)'}
                {intensity === 2 && '🤲 Level 2: Intimate Touching (Massage, erogenous zone focus, blindfolds)'}
                {intensity === 3 && '🔥 Level 3: Daring Sex Stuff (Explicit positions, physical intercourse dares, climax pacing)'}
                {intensity === 4 && '⚡ Level 4: Kink & Fantasy (Restraints, spanking, Sub/Dom dynamics, taboos)'}
              </Text>
            </View>

            <TouchableOpacity style={styles.primaryBtn} onPress={handleStartSurvey}>
              <Text style={styles.primaryBtnText}>Start Calibration Survey (8 Cards) →</Text>
            </TouchableOpacity>
          </ScrollView>
        )}

        {/* SURVEY SCREENS */}
        {(screen === 'survey_p1' || screen === 'survey_p2') && (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={styles.headerBox}>
              <Text style={styles.brandTitle}>
                {screen === 'survey_p1' ? `${partner1}'s Secret Survey` : `${partner2}'s Secret Survey`}
              </Text>
              <Text style={styles.brandSub}>
                Rate categories secretly. Red choices are blacklisted permanently.
              </Text>
            </View>

            {CATEGORIES.map((cat) => {
              const currentRating =
                screen === 'survey_p1' ? p1Survey[cat.id] : p2Survey[cat.id];

              return (
                <View key={cat.id} style={styles.card}>
                  <Text style={styles.catTitle}>{cat.title}</Text>
                  <Text style={styles.catDesc}>{cat.description}</Text>

                  <View style={styles.ratingRow}>
                    <TouchableOpacity
                      style={[styles.rateBtn, currentRating === 'green' && styles.rateGreen]}
                      onPress={() => handleRating(cat.id, 'green', screen === 'survey_p1' ? 1 : 2)}
                    >
                      <Text style={styles.rateText}>🟢 Hell Yes</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                      style={[styles.rateBtn, currentRating === 'yellow' && styles.rateYellow]}
                      onPress={() => handleRating(cat.id, 'yellow', screen === 'survey_p1' ? 1 : 2)}
                    >
                      <Text style={styles.rateText}>🟡 Curious</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                      style={[styles.rateBtn, currentRating === 'red' && styles.rateRed]}
                      onPress={() => handleRating(cat.id, 'red', screen === 'survey_p1' ? 1 : 2)}
                    >
                      <Text style={styles.rateText}>🔴 Pass</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              );
            })}

            {screen === 'survey_p1' ? (
              <TouchableOpacity style={styles.primaryBtn} onPress={finishP1Survey}>
                <Text style={styles.primaryBtnText}>Pass Phone to {partner2} →</Text>
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                style={styles.primaryBtn}
                onPress={finishP2SurveyAndGenerate}
                disabled={isLoading}
              >
                <Text style={styles.primaryBtnText}>
                  {isLoading ? 'Generating 8 Spicier Cards...' : '🔥 Generate 8-Card Deck'}
                </Text>
              </TouchableOpacity>
            )}
          </ScrollView>
        )}

        {/* GAME DECK SCREEN */}
        {screen === 'deck' && activeCard && (
          <ScrollView contentContainerStyle={styles.deckScrollContent}>
            <View style={styles.topControlBar}>
              <Text style={styles.deckHeader}>
                Card {currentCardIndex + 1} of {deck.length} • Lvl {intensity} Heat
              </Text>

              <TouchableOpacity style={styles.audioPillBtn} onPress={toggleAudioMute}>
                <Text style={styles.audioPillText}>
                  {isMuted ? '🔇 Audio Muted' : '🎵 Mood Music Active'}
                </Text>
              </TouchableOpacity>
            </View>

            {/* MOOD MUSIC & CUSTOM PLAYLIST SELECTOR */}
            <View style={styles.moodSelectorBox}>
              <Text style={styles.moodLabel}>🎶 SELECT YOUR MOOD MUSIC / PLAYLIST:</Text>
              <View style={styles.moodButtonsRow}>
                <TouchableOpacity
                  style={[styles.moodBtn, activeMood === 'sensual_rnb' && styles.moodBtnActive]}
                  onPress={() => handleSelectMood('sensual_rnb')}
                >
                  <Text style={styles.moodBtnText}>💋 Sensual Lounge</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.moodBtn, activeMood === 'warm_ambient' && styles.moodBtnActive]}
                  onPress={() => handleSelectMood('warm_ambient')}
                >
                  <Text style={styles.moodBtnText}>🌙 432Hz Ambient</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.moodBtn, activeMood === 'solfeggio_528' && styles.moodBtnActive]}
                  onPress={() => handleSelectMood('solfeggio_528')}
                >
                  <Text style={styles.moodBtnText}>🧘 528Hz Heart</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.moodBtn, activeMood === 'custom' && styles.moodBtnActive]}
                  onPress={() => handleSelectMood('custom')}
                >
                  <Text style={styles.moodBtnText}>🔗 Custom Link</Text>
                </TouchableOpacity>
              </View>

              {showMusicInput && (
                <View style={styles.customUrlRow}>
                  <TextInput
                    style={styles.customUrlInput}
                    value={customAudioUrl}
                    onChangeText={setCustomAudioUrl}
                    placeholder="Paste MP3 / Playlist audio URL..."
                    placeholderTextColor="#7E6B8F"
                  />
                  <TouchableOpacity style={styles.applyAudioBtn} onPress={applyCustomAudioUrl}>
                    <Text style={styles.applyAudioText}>Play 🎵</Text>
                  </TouchableOpacity>
                </View>
              )}
            </View>

            <View style={styles.gameCard}>
              <Text style={styles.cardType}>{activeCard.type.toUpperCase()}</Text>
              <Text style={styles.cardTitle}>{activeCard.title}</Text>

              {/* DYNAMIC REAL-TIME AI GENERATED NEON ARTWORK (1:1 Card Matched!) */}
              <NeonSilhouette
                pose={activeCard.stick_figure_pose || 'sensual_pose'}
                cardTitle={activeCard.title}
                actionPrompt={activeCard.action_prompt}
                cardDescription={activeCard.description}
                partner1Name={partner1}
                partner2Name={partner2}
              />

              <Text style={styles.cardDesc}>{activeCard.description}</Text>

              <View style={styles.promptBox}>
                <Text style={styles.promptLabel}>ACTION DARE PROMPT:</Text>
                <Text style={styles.promptText}>{activeCard.action_prompt}</Text>
              </View>

              {activeCard.timer_seconds && (
                <View style={styles.timerBox}>
                  {timerSeconds !== null ? (
                    <Text style={styles.timerCount}>{timerSeconds}s Remaining</Text>
                  ) : (
                    <TouchableOpacity
                      style={styles.timerBtn}
                      onPress={() => startTimer(activeCard.timer_seconds!)}
                    >
                      <Text style={styles.timerBtnText}>
                        ⏱️ Start {activeCard.timer_seconds}s Timer
                      </Text>
                    </TouchableOpacity>
                  )}
                </View>
              )}
            </View>

            <View style={styles.deckActions}>
              <TouchableOpacity style={styles.nextBtn} onPress={nextCard}>
                <Text style={styles.nextBtnText}>
                  {currentCardIndex < deck.length - 1 ? `Next Card (${currentCardIndex + 1} of ${deck.length}) →` : 'Finish Session 🔥'}
                </Text>
              </TouchableOpacity>

              <View style={styles.secondaryDeckRow}>
                <TouchableOpacity
                  style={styles.secBtn}
                  onPress={() => reRollDeck()}
                  disabled={isLoading}
                >
                  <Text style={styles.secBtnText}>
                    {isLoading ? 'Generating...' : '🎲 Re-Roll AI Deck'}
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={styles.secBtnHot}
                  onPress={escalateHeat}
                  disabled={isLoading}
                >
                  <Text style={styles.secBtnHotText}>
                    🔥 Escalate Heat (Lvl {intensity < 4 ? intensity + 1 : 1})
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          </ScrollView>
        )}

      </LinearGradient>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F0814' },
  gradient: { flex: 1 },
  scrollContent: { padding: 20 },
  deckScrollContent: { padding: 20, paddingBottom: 40 },
  headerBox: { alignItems: 'center', marginVertical: 16 },
  brandTitle: { fontSize: 36, fontWeight: '900', color: '#FF2E63', letterSpacing: 2 },
  brandSub: { fontSize: 14, color: '#A093B1', marginTop: 4, textAlign: 'center' },
  card: {
    backgroundColor: '#1E122C',
    borderRadius: 16,
    padding: 18,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#342148',
  },
  sectionTitle: { fontSize: 16, fontWeight: '700', color: '#FFF', marginBottom: 12 },
  label: { fontSize: 12, color: '#A093B1', marginTop: 8, marginBottom: 4 },
  input: {
    backgroundColor: '#130A1C',
    color: '#FFF',
    padding: 12,
    borderRadius: 10,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#3D2856',
  },
  intensityRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  lvlBtn: {
    flex: 1,
    backgroundColor: '#130A1C',
    paddingVertical: 12,
    marginHorizontal: 3,
    borderRadius: 10,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#3D2856',
  },
  lvlBtnActive: { backgroundColor: '#FF2E63', borderColor: '#FF2E63' },
  lvlText: { color: '#A093B1', fontWeight: '700' },
  lvlTextActive: { color: '#FFF' },
  intensityDesc: { color: '#E2D9F3', fontSize: 13, lineHeight: 18, fontWeight: '500' },
  primaryBtn: {
    backgroundColor: '#FF2E63',
    paddingVertical: 16,
    borderRadius: 14,
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 30,
    shadowColor: '#FF2E63',
    shadowOpacity: 0.4,
    shadowRadius: 10,
  },
  primaryBtnText: { color: '#FFF', fontSize: 18, fontWeight: '800' },
  catTitle: { fontSize: 18, fontWeight: '700', color: '#FFF' },
  catDesc: { fontSize: 13, color: '#A093B1', marginTop: 4, marginBottom: 12 },
  ratingRow: { flexDirection: 'row', justifyContent: 'space-between' },
  rateBtn: {
    flex: 1,
    backgroundColor: '#130A1C',
    paddingVertical: 10,
    marginHorizontal: 3,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#342148',
  },
  rateGreen: { backgroundColor: '#064E3B', borderColor: '#10B981' },
  rateYellow: { backgroundColor: '#78350F', borderColor: '#F59E0B' },
  rateRed: { backgroundColor: '#7F1D1D', borderColor: '#EF4444' },
  rateText: { color: '#FFF', fontSize: 12, fontWeight: '700' },
  deckHeader: { color: '#A093B1', fontSize: 13, fontWeight: '700' },
  topControlBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 14,
    paddingHorizontal: 4,
  },
  audioPillBtn: {
    backgroundColor: 'rgba(255, 46, 99, 0.18)',
    borderWidth: 1,
    borderColor: 'rgba(255, 46, 99, 0.4)',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
  },
  audioPillText: {
    color: '#FF2E63',
    fontSize: 12,
    fontWeight: '700',
  },
  moodSelectorBox: {
    backgroundColor: '#1E102E',
    borderRadius: 16,
    padding: 14,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 46, 99, 0.25)',
  },
  moodLabel: {
    color: '#A093B1',
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  moodButtonsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  moodBtn: {
    backgroundColor: '#130A1C',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#3D2856',
  },
  moodBtnActive: {
    backgroundColor: 'rgba(255, 46, 99, 0.3)',
    borderColor: '#FF2E63',
  },
  moodBtnText: {
    color: '#E2D9F3',
    fontSize: 12,
    fontWeight: '700',
  },
  customUrlRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 10,
  },
  customUrlInput: {
    flex: 1,
    backgroundColor: '#130A1C',
    color: '#FFF',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 10,
    fontSize: 13,
    borderWidth: 1,
    borderColor: '#3D2856',
  },
  applyAudioBtn: {
    backgroundColor: '#FF2E63',
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 10,
  },
  applyAudioText: {
    color: '#FFF',
    fontWeight: '800',
    fontSize: 12,
  },
  gameCard: {
    backgroundColor: '#231534',
    borderRadius: 24,
    padding: 22,
    borderWidth: 1,
    borderColor: '#4A2A6D',
  },
  cardType: { color: '#FF2E63', fontWeight: '800', letterSpacing: 1.5, fontSize: 12 },
  cardTitle: { color: '#FFF', fontSize: 24, fontWeight: '800', marginTop: 4, marginBottom: 8 },
  cardDesc: { color: '#D4C8E3', fontSize: 15, lineHeight: 20, marginVertical: 10 },
  promptBox: {
    backgroundColor: '#150B21',
    padding: 16,
    borderRadius: 14,
    borderLeftWidth: 4,
    borderLeftColor: '#FF2E63',
    marginTop: 10,
  },
  promptLabel: { color: '#FF2E63', fontSize: 11, fontWeight: '900', letterSpacing: 1 },
  promptText: { color: '#FFF', fontSize: 15, fontWeight: '600', marginTop: 4, lineHeight: 20 },
  timerBox: { marginTop: 16, alignItems: 'center' },
  timerBtn: { backgroundColor: '#3B1A5A', paddingVertical: 12, paddingHorizontal: 20, borderRadius: 12 },
  timerBtnText: { color: '#FFF', fontWeight: '700' },
  timerCount: { color: '#FF9F43', fontSize: 22, fontWeight: '900' },
  deckActions: { marginTop: 20 },
  nextBtn: { backgroundColor: '#FF2E63', paddingVertical: 16, borderRadius: 14, alignItems: 'center' },
  nextBtnText: { color: '#FFF', fontSize: 18, fontWeight: '800' },
  secondaryDeckRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 12,
    gap: 10,
  },
  secBtn: {
    flex: 1,
    backgroundColor: '#1E122C',
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#3D2856',
  },
  secBtnText: { color: '#E2D9F3', fontSize: 13, fontWeight: '700' },
  secBtnHot: {
    flex: 1,
    backgroundColor: 'rgba(255, 159, 67, 0.15)',
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255, 159, 67, 0.4)',
  },
  secBtnHotText: { color: '#FF9F43', fontSize: 13, fontWeight: '800' },
});
