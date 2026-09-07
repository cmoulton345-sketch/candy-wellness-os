# 🌶️ SPICE App — Visual Test Drive Guide

## 📱 Run the Test Build Locally

### Step 1: Navigate to the App Directory

```powershell
cd c:\Users\Joe\radical_simplicity_ai_os_joe-m\work_in_progress\spice_app\code
```

### Step 2: Install Dependencies (One Time Only)

```powershell
npm install
```

If you get errors, try:
```powershell
npm ci  # Clean install
```

### Step 3: Start Expo Dev Server

```powershell
npm start
```

This starts the Expo Metro bundler. You'll see output like:

```
Expo Go — To run your app, scan this QR code with Expo Go.
```

### Step 4: View the App

**Option A: On Your Phone (Recommended)**
1. Download **Expo Go** app (iOS App Store or Google Play)
2. Scan the QR code shown in terminal
3. App loads in ~10 seconds
4. See the visuals in real-time

**Option B: In Your Browser (Web)**
1. Press `w` in terminal to open in browser
2. Shows on `http://localhost:8081`
3. Not ideal for seeing full mobile UX, but works for testing

**Option C: On Simulator/Emulator**
- Press `i` for iOS Simulator
- Press `a` for Android Emulator

---

## 🎮 Test Drive Flow

### Welcome Screen
1. See SPICE logo and description
2. Select intensity level (1-4 fire emojis)
3. Tap "Start Test Drive"

### Game Screen
You'll see 6 demo cards in sequence:

| Card # | Pose | Intensity | Visual |
|---|---|---|---|
| 1 | Eye Contact Gaze | 1 🔥 | Two faces with line of connection |
| 2 | Hand Holding | 1 🔥 | Hands intertwined |
| 3 | Sensual Massage | 2 🔥🔥 | Hands on back, therapeutic |
| 4 | Blindfold & Trust | 2 🔥🔥 | Eyes covered, vulnerable pose |
| 5 | Slow Spooning | 3 🔥🔥🔥 | Bodies nested together |
| 6 | Explore Power Dynamics | 4 🔥🔥🔥🔥 | Restraint cuffs, power dynamic |

### What to Test

✅ **Neon Silhouettes**
- Each card shows a glowing silhouette
- Colors change by intensity:
  - Level 1: Amber (#FF9F43)
  - Level 2: Rose (#FF6B9D)
  - Level 3: Bright Rose (#FF2E63)
  - Level 4: Cyan (#00D9FF)

✅ **Visual-Action Alignment**
- Massage card → shows hands-on-back pose
- Blindfold card → shows eye cover silhouette
- Spooning card → shows intertwined bodies
- Does the visual match the description? 

✅ **Card Transitions**
- Smooth fade-in/fade-out between cards
- Silhouette scales up as it appears
- Tap "Next" or "Done" to advance

✅ **Haptic Feedback** (if on phone)
- Feel a pulse when card appears
- Click feedback on button taps
- Timer completion buzz

✅ **Timer Functionality**
- Some cards have timers (e.g., 2-minute massage)
- Tap "Start Timer" to activate
- Watch countdown
- Buzz when done

---

## 🔧 Troubleshooting

### "Module not found" error
```
npm install
```
Then try `npm start` again.

### Blank screen or crashes
1. Hard reload: Press `r` in terminal
2. Clear cache: `npm start -- --clear`
3. Delete node_modules: `rm -r node_modules && npm install`

### Can't scan QR code
1. Make sure phone & PC are on same WiFi
2. Terminal shows "LAN" address — use that instead
3. Or use Expo Go search feature to find your project

### Silhouettes not showing
- Refresh the app (press `r`)
- Ensure react-native-svg is installed: `npm install react-native-svg`

---

## 📸 What to Look For

Take screenshots/notes on:

1. **Silhouette Quality**
   - Are the poses recognizable?
   - Do the glow effects look good?
   - Is the neon aesthetic working?

2. **Visual-Action Match** (Main Pain Point to Fix)
   - Does each silhouette match the card description?
   - Eye contact → faces with connection line?
   - Massage → hands visible?
   - Blindfold → eye cover obvious?

3. **UI/UX Polish**
   - Smooth transitions?
   - Readable text on dark background?
   - Good color contrast?
   - Buttons responsive?

4. **Performance**
   - Smooth 60 FPS?
   - Cards load quickly?
   - No lag on tap?

---

## 💬 Give Feedback

After the test drive, tell me:

1. **Visual Quality**: "The neon silhouettes look [great/need work]"
2. **Alignment**: "The massage pose [does/doesn't] match the description"
3. **UI Feel**: "The transitions feel [smooth/laggy]"
4. **What's Missing**: "I notice [blank spots/missing details]"
5. **Next Priority**: "Fix [specific visual/UI element]"

---

## 🚀 Next After Test Drive

Once you confirm the visuals look good:
1. I'll update AI card generation to include `pose_type`
2. Integration with device playlists (if needed)
3. Full UI polish for 30-60 demographic
4. Beta testing with real couples

---

**Ready? Run `npm start` and let's see what SPICE looks like!**
