// src/screens/GameDeckScreen.tsx
// Main game deck with neon silhouettes + playlist integration + card generation

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  SafeAreaView,
  StyleSheet,
  Animated,
  Dimensions,
  ActivityIndicator,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import { PoseSilhouette } from '../components/PoseSilhouettes';
import localPlaylistService, { LocalPlaylist } from '../services/localPlaylistService';

const { width } = Dimensions.get('window');

interface Card {
  id: string;
  type: 'dare' | 'truth' | 'scenario';
  intensity: 1 | 2 | 3 | 4;
  title: string;
  description: string;
  poseType: string;
  category: string;
  timer_seconds?: number;
}

// DEMO CARDS FOR TESTING
const DEMO_CARDS: Card[] = [
  {
    id: '1',
    type: 'dare',
    intensity: 1,
    title: 'Eye Contact Gaze',
    description: 'Lock eyes for 2 minutes without speaking. Feel the connection.',
    poseType: 'eye_contact',
    category: 'Teasing',
    timer_seconds: 120,
  },
  {
    id: '2',
    type: 'dare',
    intensity: 1,
    title: 'Hand Holding Moment',
    description: 'Hold hands and trace each other\'s palms slowly. Notice every touch.',
    poseType: 'hand_holding',
    category: 'Teasing',
  },
  {
    id: '3',
    type: 'dare',
    intensity: 2,
    title: 'Sensual Massage',
    description: 'Give a 10-minute full-body massage. Focus on areas rarely touched.',
    poseType: 'massage',
    category: 'Intimate Touch',
    timer_seconds: 600,
  },
  {
    id: '4',
    type: 'dare',
    intensity: 2,
    title: 'Blindfold & Trust',
    description: 'One partner blindfolded. The other guides with gentle touch.',
    poseType: 'blindfolded',
    category: 'Intimate Touch',
  },
  {
    id: '5',
    type: 'dare',
    intensity: 3,
    title: 'Slow Spooning',
    description: 'Lie together in spooning position. Focus on breathing together.',
    poseType: 'spooning',
    category: 'Daring',
  },
  {
    id: '6',
    type: 'dare',
    intensity: 4,
    title: 'Explore Power Dynamics',
    description: 'One partner gently restrains the other. Communicate boundaries clearly.',
    poseType: 'restraint',
    category: 'Intensity',
  },
];

interface GameDeckScreenProps {
  selectedPlaylist?: LocalPlaylist;
  intensityLevel?: 1 | 2 | 3 | 4;
}

export const GameDeckScreen = ({
  selectedPlaylist,
  intensityLevel = 2,
}: GameDeckScreenProps) => {
  const [cards, setCards] = useState<Card[]>(DEMO_CARDS);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [fadeAnim] = useState(new Animated.Value(0));
  const [scaleAnim] = useState(new Animated.Value(0.8));
  const [loading, setLoading] = useState(false);
  const [timerActive, setTimerActive] = useState(false);
  const [timeLeft, setTimeLeft] = useState<number>(0);

  const currentCard = cards[currentIndex];
  const isLastCard = currentIndex === cards.length - 1;

  useEffect(() => {
    // Animate card entrance
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }),
    ]).start();

    // Haptic feedback on card reveal
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  }, [currentIndex]);

  useEffect(() => {
    // Timer logic
    if (!timerActive || timeLeft <= 0) return;

    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          setTimerActive(false);
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [timerActive, timeLeft]);

  const handleNextCard = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 0.8,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start(() => {
      if (!isLastCard) {
        setCurrentIndex((prev) => prev + 1);
        fadeAnim.setValue(0);
        scaleAnim.setValue(0.8);
        setTimerActive(false);
        setTimeLeft(0);
      }
    });
  };

  const handleStartTimer = () => {
    if (currentCard.timer_seconds) {
      setTimeLeft(currentCard.timer_seconds);
      setTimerActive(true);
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    }
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#0F0814', '#1A0C27', '#28113B']}
        style={styles.background}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.progressText}>
            {currentIndex + 1} / {cards.length}
          </Text>
          {selectedPlaylist && (
            <Text style={styles.playlistName}>
              🎵 {selectedPlaylist.name}
            </Text>
          )}
        </View>

        {/* Main Card Content */}
        <Animated.View
          style={[
            styles.cardContainer,
            {
              opacity: fadeAnim,
              transform: [{ scale: scaleAnim }],
            },
          ]}
        >
          {/* Neon Silhouette */}
          <View style={styles.silhouetteContainer}>
            <PoseSilhouette
              poseType={currentCard.poseType}
              intensity={currentCard.intensity}
              size={260}
            />
          </View>

          {/* Card Content */}
          <View style={styles.cardContent}>
            {/* Intensity Badge */}
            <View style={[styles.intensityBadge, { 
              backgroundColor: getIntensityColor(currentCard.intensity) 
            }]}>
              <Text style={styles.intensityText}>
                {'🔥'.repeat(currentCard.intensity)}
              </Text>
            </View>

            {/* Title */}
            <Text style={styles.cardTitle}>{currentCard.title}</Text>

            {/* Category */}
            <Text style={styles.categoryText}>{currentCard.category}</Text>

            {/* Description */}
            <Text style={styles.cardDescription}>
              {currentCard.description}
            </Text>

            {/* Timer Section */}
            {currentCard.timer_seconds && (
              <View style={styles.timerSection}>
                {timerActive ? (
                  <View style={styles.timerDisplay}>
                    <Text style={styles.timerText}>
                      {formatTime(timeLeft)}
                    </Text>
                  </View>
                ) : (
                  <TouchableOpacity
                    style={styles.startTimerButton}
                    onPress={handleStartTimer}
                  >
                    <Text style={styles.startTimerText}>
                      ⏱ Start {currentCard.timer_seconds}s Timer
                    </Text>
                  </TouchableOpacity>
                )}
              </View>
            )}
          </View>
        </Animated.View>

        {/* Action Buttons */}
        <View style={styles.buttonsContainer}>
          {isLastCard ? (
            <View style={styles.buttonRow}>
              <TouchableOpacity
                style={[styles.button, styles.finishButton]}
                onPress={() => {
                  Haptics.notificationAsync(
                    Haptics.NotificationFeedbackType.Success
                  );
                }}
              >
                <Text style={styles.finishButtonText}>🎉 Game Complete!</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <View style={styles.buttonRow}>
              <TouchableOpacity
                style={[styles.button, styles.skipButton]}
                onPress={() => {
                  Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
                  handleNextCard();
                }}
              >
                <Text style={styles.buttonText}>⏭ Next</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.button, styles.completeButton]}
                onPress={() => {
                  Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
                  handleNextCard();
                }}
              >
                <Text style={styles.buttonText}>✓ Done</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>

        {/* Debug Info */}
        <View style={styles.debugInfo}>
          <Text style={styles.debugText}>
            Pose: {currentCard.poseType} | Intensity: {currentCard.intensity}
          </Text>
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
};

// Helper function for intensity color
function getIntensityColor(intensity: 1 | 2 | 3 | 4): string {
  const colors = {
    1: '#FF9F43', // Amber
    2: '#FF6B9D', // Rose
    3: '#FF2E63', // Bright Rose
    4: '#00D9FF', // Cyan
  };
  return colors[intensity];
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F0814',
  },
  background: {
    flex: 1,
    paddingHorizontal: 20,
    backgroundColor: '#090510',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 46, 99, 0.15)',
  },
  progressText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#FF2E63',
    textTransform: 'uppercase',
    letterSpacing: 1.25,
  },
  playlistName: {
    fontSize: 12,
    color: '#D9D1EA',
    maxWidth: width * 0.52,
  },
  cardContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 24,
  },
  silhouetteContainer: {
    width: 290,
    height: 290,
    borderRadius: 28,
    backgroundColor: 'rgba(15, 10, 25, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 26,
    borderWidth: 1.2,
    borderColor: 'rgba(255, 46, 99, 0.38)',
    shadowColor: '#FF2E63',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.28,
    shadowRadius: 18,
    elevation: 10,
  },
  cardContent: {
    width: '100%',
    alignItems: 'center',
  },
  intensityBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    marginBottom: 16,
  },
  intensityText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  cardTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 8,
  },
  categoryText: {
    fontSize: 12,
    color: '#9CA3AF',
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginBottom: 16,
  },
  cardDescription: {
    fontSize: 15,
    color: '#E0E0E0',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 24,
  },
  timerSection: {
    marginTop: 16,
    alignItems: 'center',
  },
  timerDisplay: {
    backgroundColor: 'rgba(255, 46, 99, 0.1)',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#FF2E63',
  },
  timerText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF2E63',
    fontFamily: 'Courier New',
  },
  startTimerButton: {
    backgroundColor: 'rgba(255, 46, 99, 0.15)',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 10,
    borderWidth: 1.5,
    borderColor: '#FF2E63',
  },
  startTimerText: {
    color: '#FF2E63',
    fontWeight: '600',
    fontSize: 14,
  },
  buttonsContainer: {
    paddingBottom: 32,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 12,
  },
  button: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  skipButton: {
    backgroundColor: 'rgba(176, 176, 176, 0.15)',
    borderWidth: 1.5,
    borderColor: '#9CA3AF',
  },
  completeButton: {
    backgroundColor: '#FF2E63',
  },
  finishButton: {
    backgroundColor: '#10B981',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  finishButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  debugInfo: {
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 46, 99, 0.3)',
  },
  debugText: {
    fontSize: 11,
    color: '#9CA3AF',
    fontFamily: 'Courier New',
  },
});
