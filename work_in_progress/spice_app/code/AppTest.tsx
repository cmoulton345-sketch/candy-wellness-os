// AppTest.tsx - SPICE Visual Test Drive
// Run this to see the neon silhouettes and card visuals in action

import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  SafeAreaView,
  TouchableOpacity,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { GameDeckScreen } from './src/screens/GameDeckScreen';

type Screen = 'welcome' | 'game';

export default function AppTest() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('welcome');
  const [intensityLevel, setIntensityLevel] = useState<1 | 2 | 3 | 4>(2);

  // Welcome Screen
  if (currentScreen === 'welcome') {
    return (
      <SafeAreaView style={styles.container}>
        <LinearGradient
          colors={['#0F0814', '#1A0C27', '#28113B']}
          style={styles.background}
        >
          <View style={styles.welcomeContent}>
            {/* Logo */}
            <Text style={styles.logo}>🌶️ SPICE</Text>
            <Text style={styles.tagline}>Visual Test Drive</Text>

            {/* Description */}
            <View style={styles.descriptionBox}>
              <Text style={styles.description}>
                See the neon silhouettes matched to each card action.
              </Text>
              <Text style={styles.description}>
                Watch the visual-action alignment in real-time.
              </Text>
            </View>

            {/* Test Info */}
            <View style={styles.testInfoBox}>
              <Text style={styles.testInfoTitle}>✨ What You'll See:</Text>
              <Text style={styles.testInfoItem}>✓ Eye contact silhouette</Text>
              <Text style={styles.testInfoItem}>✓ Hand holding silhouette</Text>
              <Text style={styles.testInfoItem}>✓ Neck kiss silhouette</Text>
              <Text style={styles.testInfoItem}>✓ Massage silhouette</Text>
              <Text style={styles.testInfoItem}>✓ Blindfold silhouette</Text>
              <Text style={styles.testInfoItem}>✓ Spooning silhouette</Text>
              <Text style={styles.testInfoItem}>✓ Restraint silhouette (Level 4)</Text>
            </View>

            {/* Intensity Selector */}
            <View style={styles.intensitySelector}>
              <Text style={styles.selectorLabel}>Intensity Level:</Text>
              <View style={styles.buttonRow}>
                {[1, 2, 3, 4].map((level) => (
                  <TouchableOpacity
                    key={level}
                    style={[
                      styles.intensityButton,
                      intensityLevel === level && styles.intensityButtonActive,
                    ]}
                    onPress={() => setIntensityLevel(level as 1 | 2 | 3 | 4)}
                  >
                    <Text style={styles.intensityButtonText}>
                      {'🔥'.repeat(level)}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Start Button */}
            <TouchableOpacity
              style={styles.startButton}
              onPress={() => setCurrentScreen('game')}
            >
              <LinearGradient
                colors={['#FF2E63', '#FF6B9D']}
                style={styles.startButtonGradient}
              >
                <Text style={styles.startButtonText}>Start Test Drive</Text>
              </LinearGradient>
            </TouchableOpacity>

            {/* Info Footer */}
            <View style={styles.footer}>
              <Text style={styles.footerText}>
                💡 Click "Next" to scroll through 6 cards with different poses
              </Text>
            </View>
          </View>
        </LinearGradient>
      </SafeAreaView>
    );
  }

  // Game Screen
  return (
    <View style={styles.gameContainer}>
      <GameDeckScreen
        intensityLevel={intensityLevel}
      />
      <TouchableOpacity
        style={styles.backButton}
        onPress={() => setCurrentScreen('welcome')}
      >
        <Text style={styles.backButtonText}>← Back to Menu</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F0814',
  },
  gameContainer: {
    flex: 1,
  },
  background: {
    flex: 1,
    paddingHorizontal: 24,
    justifyContent: 'center',
  },
  welcomeContent: {
    flex: 1,
    justifyContent: 'space-between',
    paddingVertical: 40,
  },
  logo: {
    fontSize: 48,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 12,
  },
  tagline: {
    fontSize: 20,
    color: '#FF2E63',
    textAlign: 'center',
    fontWeight: '600',
    marginBottom: 32,
    letterSpacing: 0.5,
  },
  descriptionBox: {
    backgroundColor: 'rgba(255, 46, 99, 0.08)',
    borderRadius: 16,
    paddingHorizontal: 20,
    paddingVertical: 24,
    borderWidth: 1,
    borderColor: 'rgba(255, 46, 99, 0.2)',
    marginBottom: 24,
  },
  description: {
    fontSize: 15,
    color: '#E0E0E0',
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 12,
  },
  testInfoBox: {
    backgroundColor: 'rgba(0, 217, 255, 0.08)',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    borderWidth: 1,
    borderColor: 'rgba(0, 217, 255, 0.2)',
    marginBottom: 24,
  },
  testInfoTitle: {
    fontSize: 13,
    fontWeight: 'bold',
    color: '#00D9FF',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  testInfoItem: {
    fontSize: 12,
    color: '#B0B0B0',
    marginBottom: 6,
    lineHeight: 18,
  },
  intensitySelector: {
    marginBottom: 24,
  },
  selectorLabel: {
    fontSize: 13,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 10,
  },
  intensityButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 10,
    backgroundColor: 'rgba(176, 176, 176, 0.1)',
    borderWidth: 1.5,
    borderColor: '#9CA3AF',
    alignItems: 'center',
  },
  intensityButtonActive: {
    backgroundColor: 'rgba(255, 46, 99, 0.2)',
    borderColor: '#FF2E63',
  },
  intensityButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  startButton: {
    borderRadius: 14,
    overflow: 'hidden',
    marginBottom: 16,
  },
  startButtonGradient: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  startButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  footer: {
    backgroundColor: 'rgba(255, 159, 67, 0.1)',
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: 'rgba(255, 159, 67, 0.3)',
  },
  footerText: {
    fontSize: 12,
    color: '#FFB347',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  backButton: {
    position: 'absolute',
    top: 16,
    left: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(255, 46, 99, 0.4)',
    zIndex: 100,
  },
  backButtonText: {
    color: '#FF2E63',
    fontSize: 13,
    fontWeight: 'bold',
  },
});
