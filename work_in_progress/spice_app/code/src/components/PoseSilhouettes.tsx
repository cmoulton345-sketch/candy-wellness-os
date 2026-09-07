// src/components/PoseSilhouettes.tsx
// Clear, expressive couple silhouettes in a neon line-art style.

import React from 'react';
import Svg, { Path, Circle, Defs, Filter, FeGaussianBlur, FeMerge, FeMergeNode } from 'react-native-svg';

interface SilhouetteProps {
  intensity: 1 | 2 | 3 | 4;
  poseType: string;
  color?: string;
  size?: number;
}

const rose = '#FF2E63';
const blue = '#5B7CFF';
const purple = '#A855F7';
const amber = '#FF9F43';

const getAccent = (intensity: 1 | 2 | 3 | 4) => {
  if (intensity === 4) return purple;
  if (intensity === 3) return rose;
  if (intensity === 2) return '#FF6B9D';
  return amber;
};

const makeGlow = (id: string) => (
  <Defs key={id}>
    <Filter id={id}>
      <FeGaussianBlur stdDeviation="2.5" result="blur" />
      <FeMerge>
        <FeMergeNode in="blur" />
        <FeMergeNode in="SourceGraphic" />
      </FeMerge>
    </Filter>
  </Defs>
);

export const EyeContactGaze = ({ intensity = 1, size = 220 }: SilhouetteProps) => {
  const glowId = 'eyeGlow';
  return (
    <Svg width={size} height={size} viewBox="0 0 220 260">
      {makeGlow(glowId)}
      <Circle cx="72" cy="78" r="26" stroke={rose} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Circle cx="148" cy="78" r="26" stroke={blue} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 70 112 Q 110 152 150 112" stroke={getAccent(intensity)} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 80 158 Q 110 182 140 158" stroke={getAccent(intensity)} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 66 106 L 78 100" stroke={rose} strokeWidth="2" filter={`url(#${glowId})`} />
      <Path d="M 154 106 L 142 100" stroke={blue} strokeWidth="2" filter={`url(#${glowId})`} />
    </Svg>
  );
};

export const HandHolding = ({ intensity = 1, size = 220 }: SilhouetteProps) => {
  const glowId = 'handGlow';
  return (
    <Svg width={size} height={size} viewBox="0 0 220 260">
      {makeGlow(glowId)}
      <Path d="M 52 112 Q 70 96 92 120 Q 100 128 96 140 Q 82 160 62 160 Q 46 158 42 138 Z" stroke={rose} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 168 112 Q 150 96 128 120 Q 120 128 124 140 Q 138 160 158 160 Q 174 158 178 138 Z" stroke={blue} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 88 128 Q 110 138 132 128" stroke={getAccent(intensity)} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 92 146 Q 110 154 128 146" stroke={getAccent(intensity)} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
    </Svg>
  );
};

export const NeckKiss = ({ intensity = 1, size = 220 }: SilhouetteProps) => {
  const glowId = 'neckGlow';
  return (
    <Svg width={size} height={size} viewBox="0 0 220 260">
      {makeGlow(glowId)}
      <Circle cx="116" cy="66" r="27" stroke={blue} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 92 92 Q 78 120 82 146 Q 88 174 104 186" stroke={rose} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 136 110 Q 152 122 158 142" stroke={blue} strokeWidth="2.3" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 122 112 Q 138 118 146 132" stroke={getAccent(intensity)} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 131 118 Q 148 124 156 138" stroke={getAccent(intensity)} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
    </Svg>
  );
};

export const Massage = ({ intensity = 2, size = 220 }: SilhouetteProps) => {
  const glowId = 'massageGlow';
  return (
    <Svg width={size} height={size} viewBox="0 0 220 260">
      {makeGlow(glowId)}
      <Path d="M 110 40 C 96 52, 90 74, 90 110 L 90 170 C 90 186, 98 196, 110 196 C 122 196, 130 186, 130 170 L 130 110 C 130 74, 124 52, 110 40 Z" stroke={rose} strokeWidth="2.3" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 68 110 C 48 114, 44 100, 44 88 C 44 70, 60 68, 70 82" stroke={rose} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 152 110 C 172 114, 176 100, 176 88 C 176 70, 160 68, 150 82" stroke={blue} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 78 148 Q 96 142 110 152 Q 124 142 142 148" stroke={getAccent(intensity)} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
    </Svg>
  );
};

export const Blindfolded = ({ intensity = 2, size = 220 }: SilhouetteProps) => {
  const glowId = 'blindfoldGlow';
  return (
    <Svg width={size} height={size} viewBox="0 0 220 260">
      {makeGlow(glowId)}
      <Circle cx="110" cy="66" r="28" stroke={rose} strokeWidth="2.2" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 68 62 H 152 V 72 H 68 Z" stroke={blue} strokeWidth="3" fill={blue} opacity="0.2" filter={`url(#${glowId})`} />
      <Path d="M 92 96 Q 82 118 86 148 Q 92 180 110 188 Q 128 180 134 148 Q 138 118 128 96 Z" stroke={rose} strokeWidth="2.3" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 76 120 C 58 128, 54 142, 60 156" stroke={blue} strokeWidth="2.1" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 144 120 C 162 128, 166 142, 160 156" stroke={blue} strokeWidth="2.1" fill="none" filter={`url(#${glowId})`} />
    </Svg>
  );
};

export const Spooning = ({ intensity = 3, size = 220 }: SilhouetteProps) => {
  const glowId = 'spooningGlow';
  return (
    <Svg width={size} height={size} viewBox="0 0 220 260">
      {makeGlow(glowId)}
      <Path d="M 74 72 C 58 94, 58 136, 70 176 Q 77 196, 92 200 C 108 204, 120 192, 120 170 L 120 100 C 120 78, 108 64, 92 62 C 84 60, 78 64, 74 72 Z" stroke={rose} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 122 78 C 138 96, 148 124, 146 158 Q 144 180, 128 196 C 112 212, 94 190, 90 170 L 90 120 C 90 96, 100 82, 116 78 C 120 76, 121 76, 122 78 Z" stroke={blue} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 96 134 Q 110 142 124 134" stroke={getAccent(intensity)} strokeWidth="2.1" fill="none" filter={`url(#${glowId})`} />
    </Svg>
  );
};

export const Restraint = ({ intensity = 4, size = 220 }: SilhouetteProps) => {
  const glowId = 'restraintGlow';
  return (
    <Svg width={size} height={size} viewBox="0 0 220 260">
      {makeGlow(glowId)}
      <Circle cx="110" cy="56" r="23" stroke={rose} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 92 84 Q 78 120 78 160 Q 78 182 88 194" stroke={rose} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 128 84 Q 142 120 142 160 Q 142 182 132 194" stroke={blue} strokeWidth="2.4" fill="none" filter={`url(#${glowId})`} />
      <Path d="M 68 100 H 84" stroke={getAccent(intensity)} strokeWidth="2.2" filter={`url(#${glowId})`} />
      <Path d="M 136 100 H 152" stroke={getAccent(intensity)} strokeWidth="2.2" filter={`url(#${glowId})`} />
      <Path d="M 72 154 H 88" stroke={getAccent(intensity)} strokeWidth="2.2" filter={`url(#${glowId})`} />
      <Path d="M 132 154 H 148" stroke={getAccent(intensity)} strokeWidth="2.2" filter={`url(#${glowId})`} />
      <Circle cx="76" cy="100" r="7" stroke={rose} strokeWidth="2" fill="none" filter={`url(#${glowId})`} />
      <Circle cx="144" cy="100" r="7" stroke={blue} strokeWidth="2" fill="none" filter={`url(#${glowId})`} />
      <Circle cx="80" cy="154" r="7" stroke={rose} strokeWidth="2" fill="none" filter={`url(#${glowId})`} />
      <Circle cx="140" cy="154" r="7" stroke={blue} strokeWidth="2" fill="none" filter={`url(#${glowId})`} />
    </Svg>
  );
};

export const PoseSilhouette = (props: SilhouetteProps) => {
  const poseMap: { [key: string]: React.FC<SilhouetteProps> } = {
    eye_contact: EyeContactGaze,
    hand_holding: HandHolding,
    neck_kiss: NeckKiss,
    massage: Massage,
    blindfolded: Blindfolded,
    spooning: Spooning,
    restraint: Restraint,
  };

  const Component = poseMap[props.poseType] || EyeContactGaze;
  return <Component {...props} />;
};
