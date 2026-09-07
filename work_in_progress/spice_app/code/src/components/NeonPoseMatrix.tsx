import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Svg, { Circle, Line, Path, G, Defs, LinearGradient as SvgGradient, Stop } from 'react-native-svg';

export type PoseCategory =
  | 'massage'
  | 'kiss'
  | 'blindfold'
  | 'embraced'
  | 'sensual_pose'
  | 'wild_position'
  | 'kink_bondage'
  | 'lotus'
  | 'elevated_arch'
  | 'spanking';

interface Props {
  pose?: PoseCategory | string;
  partner1Name?: string;
  partner2Name?: string;
}

export const NeonPoseMatrix: React.FC<Props> = ({
  pose = 'sensual_pose',
  partner1Name = 'Partner 1',
  partner2Name = 'Partner 2',
}) => {
  const pink = '#FF2E63'; // Partner A (Neon Rose Pink)
  const purple = '#A855F7'; // Partner B (Neon Electric Purple)
  const cyan = '#00F2FE'; // Accent motion glow

  const normalizedPose: PoseCategory = (
    [
      'massage',
      'kiss',
      'blindfold',
      'embraced',
      'sensual_pose',
      'wild_position',
      'kink_bondage',
      'lotus',
      'elevated_arch',
      'spanking',
    ].includes(pose)
      ? pose
      : 'sensual_pose'
  ) as PoseCategory;

  return (
    <View style={styles.container}>
      <Svg height="160" width="260" viewBox="0 0 240 160">
        <Defs>
          <SvgGradient id="pinkGlow" x1="0" y1="0" x2="1" y2="1">
            <Stop offset="0%" stopColor="#FF2E63" stopOpacity="1" />
            <Stop offset="100%" stopColor="#FF8E53" stopOpacity="0.8" />
          </SvgGradient>
          <SvgGradient id="purpleGlow" x1="0" y1="0" x2="1" y2="1">
            <Stop offset="0%" stopColor="#A855F7" stopOpacity="1" />
            <Stop offset="100%" stopColor="#6366F1" stopOpacity="0.8" />
          </SvgGradient>
        </Defs>

        <G strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round">
          {/* POSE: Kiss / Sensual Embrace */}
          {(normalizedPose === 'kiss' || normalizedPose === 'sensual_pose' || normalizedPose === 'embraced') && (
            <>
              {/* Partner A (Pink - Left) */}
              <Circle cx="95" cy="45" r="13" stroke={pink} fill="none" />
              <Line x1="95" y1="58" x2="95" y2="100" stroke={pink} />
              <Line x1="95" y1="72" x2="125" y2="60" stroke={pink} />
              <Line x1="95" y1="100" x2="75" y2="140" stroke={pink} />
              <Line x1="95" y1="100" x2="110" y2="140" stroke={pink} />

              {/* Partner B (Purple - Right) */}
              <Circle cx="145" cy="45" r="13" stroke={purple} fill="none" />
              <Line x1="145" y1="58" x2="145" y2="100" stroke={purple} />
              <Line x1="145" y1="72" x2="115" y2="60" stroke={purple} />
              <Line x1="145" y1="100" x2="130" y2="140" stroke={purple} />
              <Line x1="145" y1="100" x2="165" y2="140" stroke={purple} />

              {/* Heart/Energy Arc */}
              <Path d="M 120 28 Q 120 20 115 20 Q 110 20 110 26 Q 110 32 120 40 Q 130 32 130 26 Q 130 20 125 20 Q 120 20 120 28" fill={pink} opacity="0.8" />
            </>
          )}

          {/* POSE: Back / Erogenous Massage */}
          {normalizedPose === 'massage' && (
            <>
              {/* Partner B Lying Down (Purple) */}
              <Circle cx="180" cy="95" r="13" stroke={purple} fill="none" />
              <Line x1="70" y1="105" x2="167" y2="105" stroke={purple} />
              <Line x1="70" y1="105" x2="50" y2="128" stroke={purple} />

              {/* Partner A Kneeling Over (Pink) */}
              <Circle cx="105" cy="50" r="13" stroke={pink} fill="none" />
              <Line x1="105" y1="63" x2="100" y2="95" stroke={pink} />
              <Line x1="105" y1="72" x2="130" y2="95" stroke={pink} />
              <Line x1="105" y1="72" x2="150" y2="95" stroke={pink} />
              <Line x1="100" y1="95" x2="80" y2="128" stroke={pink} />

              {/* Massage Glow Ripple */}
              <Circle cx="138" cy="95" r="8" stroke={cyan} strokeWidth="2" strokeDasharray="3,3" fill="none" opacity="0.7" />
            </>
          )}

          {/* POSE: Sensory Blindfold */}
          {normalizedPose === 'blindfold' && (
            <>
              {/* Partner A Standing Seated (Pink) */}
              <Circle cx="90" cy="45" r="13" stroke={pink} fill="none" />
              <Line x1="90" y1="58" x2="90" y2="100" stroke={pink} />
              <Line x1="90" y1="70" x2="125" y2="45" stroke={pink} /> {/* Reaching for blindfold */}
              <Line x1="90" y1="100" x2="70" y2="140" stroke={pink} />

              {/* Partner B Blindfolded (Purple) */}
              <Circle cx="140" cy="45" r="13" stroke={purple} fill="none" />
              {/* Blindfold Bar */}
              <Line x1="130" y1="45" x2="150" y2="45" stroke={cyan} strokeWidth="6" />
              <Line x1="140" y1="58" x2="140" y2="100" stroke={purple} />
              <Line x1="140" y1="75" x2="115" y2="90" stroke={purple} />
              <Line x1="140" y1="100" x2="155" y2="140" stroke={purple} />
            </>
          )}

          {/* POSE: Seated Lotus Embrace */}
          {(normalizedPose === 'lotus' || normalizedPose === 'wild_position') && (
            <>
              {/* Partner A Base Seated Cross-legged (Pink) */}
              <Circle cx="120" cy="40" r="13" stroke={pink} fill="none" />
              <Line x1="120" y1="53" x2="120" y2="95" stroke={pink} />
              <Line x1="120" y1="95" x2="90" y2="125" stroke={pink} />
              <Line x1="120" y1="95" x2="150" y2="125" stroke={pink} />

              {/* Partner B Wrapped Around (Purple) */}
              <Circle cx="125" cy="42" r="13" stroke={purple} fill="none" />
              <Line x1="125" y1="55" x2="125" y2="95" stroke={purple} />
              <Line x1="125" y1="68" x2="100" y2="78" stroke={purple} /> {/* Wraps around back */}
              <Line x1="125" y1="95" x2="100" y2="115" stroke={purple} />
              <Line x1="125" y1="95" x2="150" y2="115" stroke={purple} />
            </>
          )}

          {/* POSE: Elevated Arch / Bridge */}
          {normalizedPose === 'elevated_arch' && (
            <>
              {/* Partner B Arching (Purple) */}
              <Circle cx="60" cy="115" r="13" stroke={purple} fill="none" />
              <Path d="M 60 105 Q 120 40 180 105" fill="none" stroke={purple} strokeWidth="4.5" />
              <Line x1="180" y1="105" x2="195" y2="135" stroke={purple} />

              {/* Partner A Standing Over (Pink) */}
              <Circle cx="120" cy="35" r="13" stroke={pink} fill="none" />
              <Line x1="120" y1="48" x2="120" y2="85" stroke={pink} />
              <Line x1="120" y1="62" x2="145" y2="75" stroke={pink} />
              <Line x1="120" y1="85" x2="105" y2="135" stroke={pink} />
              <Line x1="120" y1="85" x2="135" y2="135" stroke={pink} />
            </>
          )}

          {/* POSE: Spanking / Power Dynamic */}
          {(normalizedPose === 'spanking' || normalizedPose === 'kink_bondage') && (
            <>
              {/* Partner A Standing Dominant (Pink) */}
              <Circle cx="80" cy="40" r="13" stroke={pink} fill="none" />
              <Line x1="80" y1="53" x2="80" y2="95" stroke={pink} />
              <Line x1="80" y1="68" x2="125" y2="75" stroke={pink} /> {/* Raised hand */}
              <Line x1="80" y1="95" x2="60" y2="138" stroke={pink} />
              <Line x1="80" y1="95" x2="95" y2="138" stroke={pink} />

              {/* Partner B Bent Over Lap (Purple) */}
              <Circle cx="170" cy="95" r="13" stroke={purple} fill="none" />
              <Line x1="105" y1="85" x2="160" y2="88" stroke={purple} />
              <Line x1="105" y1="85" x2="95" y2="115" stroke={purple} />
              <Line x1="160" y1="88" x2="185" y2="125" stroke={purple} />

              {/* Impact Flash Spark */}
              <Path d="M 130 65 L 140 70 L 132 75 L 145 80" fill="none" stroke={cyan} strokeWidth="3" />
            </>
          )}
        </G>
      </Svg>

      <View style={styles.legendRow}>
        <View style={styles.legendItem}>
          <View style={[styles.dot, { backgroundColor: pink }]} />
          <Text style={styles.legendText}>{partner1Name}</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.dot, { backgroundColor: purple }]} />
          <Text style={styles.legendText}>{partner2Name}</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: 210,
    borderRadius: 20,
    marginVertical: 10,
    borderWidth: 1.5,
    borderColor: 'rgba(255, 46, 99, 0.35)',
    backgroundColor: '#090312',
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 8,
  },
  legendRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 4,
    gap: 20,
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
    color: '#9CA3AF',
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
});
