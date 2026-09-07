import React from 'react';
import { View, StyleSheet, Image, ImageSourcePropType, Text } from 'react-native';

interface Props {
  pose?: string;
  cardTitle?: string;
  actionPrompt?: string;
  cardDescription?: string;
  partner1Name?: string;
  partner2Name?: string;
}

// Master 1:1 High-Resolution Neon Pose Artwork Matrix
const poseImages: Record<string, ImageSourcePropType> = {
  blindfold: require('../../assets/images/blindfold.png'),
  spanking: require('../../assets/images/spanking.png'),
  massage: require('../../assets/images/massage.png'),
  kiss: require('../../assets/images/kiss.png'),
  embraced: require('../../assets/images/kiss.png'),
  lotus: require('../../assets/images/lotus.png'),
  kink_bondage: require('../../assets/images/kink_bondage.png'),
  strip_tease: require('../../assets/images/strip_tease.png'),
  temperature_play: require('../../assets/images/temperature_play.png'),
  roleplay_fantasy: require('../../assets/images/roleplay_fantasy.png'),
  wild_position: require('../../assets/images/wild_position.png'),
  elevated_arch: require('../../assets/images/wild_position.png'),
  sensual_pose: require('../../assets/images/sensual_pose.png'),
};

// Intelligently maps card title, description, and pose type to the exact matching high-res neon artwork
function resolvePoseImage(pose?: string, title?: string, prompt?: string, description?: string): ImageSourcePropType {
  // 1. If explicit non-generic pose key is specified, use it directly
  if (pose && poseImages[pose] && pose !== 'sensual_pose') {
    return poseImages[pose];
  }

  // 2. Keyword analysis across title, action prompt, and description
  const text = `${title || ''} ${prompt || ''} ${description || ''}`.toLowerCase();

  if (text.includes('blindfold') || text.includes('sensory') || text.includes('eyes') || text.includes('tease')) {
    return poseImages.blindfold;
  }
  if (text.includes('spank') || text.includes('whip') || text.includes('discipline') || text.includes('fours') || text.includes('bottom') || text.includes('power') || text.includes('butt') || text.includes('hip')) {
    return poseImages.spanking;
  }
  if (text.includes('massage') || text.includes('oil') || text.includes('touch') || text.includes('rub') || text.includes('back') || text.includes('shoulder')) {
    return poseImages.massage;
  }
  if (text.includes('kiss') || text.includes('mouth') || text.includes('lips') || text.includes('embrace') || text.includes('neck')) {
    return poseImages.kiss;
  }
  if (text.includes('lotus') || text.includes('straddle') || text.includes('lap') || text.includes('seated') || text.includes('thigh')) {
    return poseImages.lotus;
  }
  if (text.includes('bondage') || text.includes('tie') || text.includes('restraint') || text.includes('cuff') || text.includes('sub') || text.includes('bound')) {
    return poseImages.kink_bondage;
  }
  if (text.includes('strip') || text.includes('flirt') || text.includes('striptease') || text.includes('clothes') || text.includes('undress')) {
    return poseImages.strip_tease;
  }
  if (text.includes('ice') || text.includes('warmth') || text.includes('contrast') || text.includes('temperature') || text.includes('cold') || text.includes('heat')) {
    return poseImages.temperature_play;
  }
  if (text.includes('roleplay') || text.includes('stranger') || text.includes('fantasy') || text.includes('alter-ego') || text.includes('role') || text.includes('pretend')) {
    return poseImages.roleplay_fantasy;
  }
  if (text.includes('wild') || text.includes('position') || text.includes('ride') || text.includes('intercourse') || text.includes('climax') || text.includes('sex')) {
    return poseImages.wild_position;
  }

  // 3. Fallback to generic sensual pose only when no specific keywords match
  return poseImages.sensual_pose;
}

export const NeonSilhouette: React.FC<Props> = ({
  pose = 'sensual_pose',
  cardTitle = '',
  actionPrompt = '',
  cardDescription = '',
  partner1Name = 'Joe',
  partner2Name = 'Candy',
}) => {
  const selectedImage = resolvePoseImage(pose, cardTitle, actionPrompt, cardDescription);

  return (
    <View style={styles.container}>
      <Image
        source={selectedImage}
        style={styles.heroImage}
        resizeMode="contain"
      />
      {/* Partner Legend Overlay */}
      <View style={styles.legendOverlay}>
        <View style={styles.legendItem}>
          <View style={[styles.dot, { backgroundColor: '#2E7BC4' }]} />
          <Text style={styles.legendText}>{partner1Name} (Male)</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.dot, { backgroundColor: '#FF2E63' }]} />
          <Text style={styles.legendText}>{partner2Name} (Female)</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: 350,
    borderRadius: 20,
    overflow: 'hidden',
    marginVertical: 14,
    borderWidth: 1.5,
    borderColor: 'rgba(255, 46, 147, 0.45)',
    backgroundColor: '#080210',
    shadowColor: '#FF2E63',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.6,
    shadowRadius: 20,
    justify.content: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  heroImage: {
    width: '100%',
    height: '100%',
  },
  legendOverlay: {
    position: 'absolute',
    bottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justify.content: 'center',
    gap: 16,
    backgroundColor: 'rgba(10, 3, 18, 0.85)',
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(255, 46, 99, 0.3)',
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  legendText: {
    color: '#E2D9F3',
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
});
