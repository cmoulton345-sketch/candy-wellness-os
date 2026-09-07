import React from 'react';
import { View, StyleSheet } from 'react-native';
import Svg, { Circle, Line, Path, G } from 'react-native-svg';

interface Props {
  pose?: 'massage' | 'kiss' | 'blindfold' | 'embraced' | 'sensual_pose' | 'wild_position' | 'kink_bondage';
}

export const NeonStickFigure: React.FC<Props> = ({ pose = 'sensual_pose' }) => {
  const pink = '#FF2E63'; // Partner A (Neon Pink)
  const purple = '#A855F7'; // Partner B (Neon Purple)

  return (
    <View style={styles.container}>
      <Svg height="140" width="220" viewBox="0 0 200 140">
        <G strokeWidth="4" strokeLinecap="round">

          {/* POSE 1: Intimate Kiss / Embrace */}
          {(pose === 'kiss' || pose === 'sensual_pose') && (
            <>
              {/* Partner A (Pink - Left) */}
              <Circle cx="80" cy="40" r="12" stroke={pink} fill="none" />
              <Line x1="80" y1="52" x2="80" y2="90" stroke={pink} />
              <Line x1="80" y1="65" x2="105" y2="55" stroke={pink} /> {/* Reaching Arm */}
              <Line x1="80" y1="90" x2="65" y2="125" stroke={pink} />
              <Line x1="80" y1="90" x2="95" y2="125" stroke={pink} />

              {/* Partner B (Purple - Right) */}
              <Circle cx="120" cy="40" r="12" stroke={purple} fill="none" />
              <Line x1="120" y1="52" x2="120" y2="90" stroke={purple} />
              <Line x1="120" y1="65" x2="95" y2="55" stroke={purple} /> {/* Embracing Arm */}
              <Line x1="120" y1="90" x2="105" y2="125" stroke={purple} />
              <Line x1="120" y1="90" x2="135" y2="125" stroke={purple} />
            </>
          )}

          {/* POSE 2: Back Massage / Touch */}
          {pose === 'massage' && (
            <>
              {/* Partner B Lying Down (Purple) */}
              <Circle cx="150" cy="85" r="12" stroke={purple} fill="none" />
              <Line x1="60" y1="95" x2="140" y2="95" stroke={purple} /> {/* Body */}
              <Line x1="60" y1="95" x2="45" y2="115" stroke={purple} />

              {/* Partner A Kneeling Over (Pink) */}
              <Circle cx="90" cy="45" r="12" stroke={pink} fill="none" />
              <Line x1="90" y1="57" x2="85" y2="85" stroke={pink} />
              <Line x1="90" y1="65" x2="110" y2="88" stroke={pink} /> {/* Massaging Arms */}
              <Line x1="85" y1="85" x2="70" y2="115" stroke={pink} />
            </>
          )}

          {/* POSE 3: Wild Position / Lotus */}
          {pose === 'wild_position' && (
            <>
              {/* Partner A Seated (Pink) */}
              <Circle cx="100" cy="35" r="12" stroke={pink} fill="none" />
              <Line x1="100" y1="47" x2="100" y2="85" stroke={pink} />
              <Line x1="100" y1="60" x2="75" y2="75" stroke={pink} />
              <Line x1="100" y1="85" x2="70" y2="115" stroke={pink} />
              <Line x1="100" y1="85" x2="130" y2="115" stroke={pink} />

              {/* Partner B Wrapped (Purple) */}
              <Circle cx="108" cy="38" r="12" stroke={purple} fill="none" />
              <Line x1="108" y1="50" x2="115" y2="85" stroke={purple} />
              <Line x1="108" y1="60" x2="85" y2="55" stroke={purple} />
              <Path d="M 115 85 Q 140 70 100 100" stroke={purple} fill="none" />
            </>
          )}

          {/* POSE 4: Blindfold & Sensory */}
          {pose === 'blindfold' && (
            <>
              {/* Partner B Blindfolded (Purple) */}
              <Circle cx="110" cy="45" r="12" stroke={purple} fill="none" />
              <Line x1="98" y1="45" x2="122" y2="45" stroke="#FF2E63" strokeWidth="6" /> {/* Neon Blindfold Strap */}
              <Line x1="110" y1="57" x2="110" y2="95" stroke={purple} />
              <Line x1="110" y1="95" x2="95" y2="130" stroke={purple} />
              <Line x1="110" y1="95" x2="125" y2="130" stroke={purple} />

              {/* Partner A Approaching (Pink) */}
              <Circle cx="60" cy="45" r="12" stroke={pink} fill="none" />
              <Line x1="60" y1="57" x2="60" y2="95" stroke={pink} />
              <Line x1="60" y1="65" x2="95" y2="60" stroke={pink} /> {/* Feather/Touch arm */}
              <Line x1="60" y1="95" x2="45" y2="130" stroke={pink} />
            </>
          )}

          {/* POSE 5: Kink & Restraints */}
          {pose === 'kink_bondage' && (
            <>
              {/* Partner B Bound (Purple) */}
              <Circle cx="120" cy="40" r="12" stroke={purple} fill="none" />
              <Line x1="120" y1="52" x2="120" y2="90" stroke={purple} />
              <Circle cx="120" cy="65" r="6" stroke="#FF9F43" strokeWidth="3" fill="none" /> {/* Wrist Cuffs */}
              <Line x1="120" y1="90" x2="105" y2="125" stroke={purple} />
              <Line x1="120" y1="90" x2="135" y2="125" stroke={purple} />

              {/* Partner A Dominant Standing (Pink) */}
              <Circle cx="70" cy="35" r="12" stroke={pink} fill="none" />
              <Line x1="70" y1="47" x2="70" y2="90" stroke={pink} />
              <Line x1="70" y1="60" x2="105" y2="65" stroke={pink} strokeDasharray="3,3" /> {/* Restraint Tether */}
              <Line x1="70" y1="90" x2="55" y2="125" stroke={pink} />
              <Line x1="70" y1="90" x2="85" y2="125" stroke={pink} />
            </>
          )}

          {/* POSE 6: Deep Embrace */}
          {pose === 'embraced' && (
            <>
              <Circle cx="95" cy="40" r="12" stroke={pink} fill="none" />
              <Circle cx="105" cy="40" r="12" stroke={purple} fill="none" />
              <Path d="M 80 90 Q 100 50 120 90" stroke={pink} fill="none" />
              <Path d="M 90 90 Q 100 50 110 90" stroke={purple} fill="none" />
              <Line x1="90" y1="90" x2="80" y2="125" stroke={pink} />
              <Line x1="110" y1="90" x2="120" y2="125" stroke={purple} />
            </>
          )}

        </G>
      </Svg>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 10,
    padding: 8,
    backgroundColor: '#130A1C',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#3D225A',
  },
});
