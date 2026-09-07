// Custom Mood Music & Playlist Engine for SPICE
// Allows couples to select mood playlists or input their custom music stream / MP3 URLs.

export type MoodGenre = 'sensual_rnb' | 'warm_ambient' | 'solfeggio_528' | 'romantic_acoustic' | 'custom';

class SoundscapeEngine {
  private isMuted: boolean = false;
  private volume: number = 0.5;
  private currentGenre: MoodGenre = 'sensual_rnb';
  private customUrl: string = '';
  private bgAudioElement: HTMLAudioElement | null = null;

  // Curated High-Quality Mood Playlists (Smooth, Sensual, Zero Rock Drums)
  private moodStreams: Record<MoodGenre, string> = {
    sensual_rnb: 'https://cdn.pixabay.com/download/audio/2022/10/25/audio_24e3c23945.mp3?filename=sensual-lounge-ambient-124908.mp3',
    warm_ambient: 'https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=ambient-piano-amp-strings-10711.mp3',
    solfeggio_528: 'https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a8c4f4.mp3?filename=meditation-relaxing-music-10842.mp3',
    romantic_acoustic: 'https://cdn.pixabay.com/download/audio/2021/08/09/audio_884488fa4d.mp3?filename=meditation-ambient-pad-88448.mp3',
    custom: '',
  };

  public setMuted(muted: boolean) {
    this.isMuted = muted;
    if (this.isMuted) {
      this.stop();
    } else {
      this.playCurrentMood();
    }
  }

  public getIsMuted(): boolean {
    return this.isMuted;
  }

  public setVolume(vol: number) {
    this.volume = Math.max(0, Math.min(1, vol));
    if (this.bgAudioElement) {
      this.bgAudioElement.volume = this.volume;
    }
  }

  public setMoodGenre(genre: MoodGenre, customAudioUrl?: string) {
    this.currentGenre = genre;
    if (customAudioUrl) {
      this.customUrl = customAudioUrl;
    }
    if (!this.isMuted) {
      this.playCurrentMood();
    }
  }

  public getCurrentGenre(): MoodGenre {
    return this.currentGenre;
  }

  public stop() {
    if (this.bgAudioElement) {
      try {
        this.bgAudioElement.pause();
        this.bgAudioElement.currentTime = 0;
      } catch (e) {}
      this.bgAudioElement = null;
    }
  }

  public playCurrentMood() {
    if (this.isMuted) return;
    this.stop();

    if (typeof window === 'undefined' || typeof Audio === 'undefined') return;

    let targetUrl = this.moodStreams[this.currentGenre];
    if (this.currentGenre === 'custom' && this.customUrl.trim().length > 0) {
      targetUrl = this.customUrl.trim();
    }

    if (!targetUrl) return;

    try {
      const audio = new Audio(targetUrl);
      audio.loop = true;
      audio.volume = this.volume;
      audio.play().then(() => {
        this.bgAudioElement = audio;
      }).catch((err) => {
        console.warn('Audio playback prevented or restricted:', err);
      });
    } catch (e) {
      console.error('Failed to play mood music:', e);
    }
  }

  public playForIntensity(level: number) {
    // Automatically pick mood matching intensity level if user hasn't explicitly selected custom
    if (this.currentGenre !== 'custom') {
      const levelMap: Record<number, MoodGenre> = {
        1: 'warm_ambient',
        2: 'solfeggio_528',
        3: 'sensual_rnb',
        4: 'romantic_acoustic',
      };
      this.currentGenre = levelMap[level] || 'sensual_rnb';
    }
    this.playCurrentMood();
  }
}

export const soundscapeEngine = new SoundscapeEngine();
