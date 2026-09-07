// src/services/localPlaylistService.ts
// Access device's native music library - NO external APIs required

import { Audio } from 'expo-av';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as MediaLibrary from 'expo-media-library';

export interface LocalPlaylist {
  id: string;
  name: string;
  trackCount: number;
  duration: number; // in seconds
  albumArt?: string;
}

export interface Song {
  id: string;
  title: string;
  artist: string;
  album: string;
  duration: number;
  uri: string;
  albumArt?: string;
}

class LocalPlaylistService {
  private currentSound: Audio.Sound | null = null;
  private isPlaying: boolean = false;
  private currentPlaylist: LocalPlaylist | null = null;

  /**
   * Request permission to access device music library
   */
  async requestPermission(): Promise<boolean> {
    try {
      const permission = await MediaLibrary.requestPermissionsAsync();
      return permission.granted;
    } catch (error) {
      console.error('Permission request failed:', error);
      return false;
    }
  }

  /**
   * Get all playlists from device
   */
  async getDevicePlaylists(): Promise<LocalPlaylist[]> {
    try {
      const hasPermission = await this.requestPermission();
      if (!hasPermission) return [];

      const playlists = await MediaLibrary.getPlaylistsAsync();

      return playlists.map((playlist) => ({
        id: playlist.id,
        name: playlist.name,
        trackCount: playlist.assetCount,
        duration: 0, // Would need to sum all tracks
        albumArt: undefined,
      }));
    } catch (error) {
      console.error('Failed to fetch playlists:', error);
      return [];
    }
  }

  /**
   * Get songs from a specific playlist
   */
  async getPlaylistSongs(playlistId: string): Promise<Song[]> {
    try {
      const hasPermission = await this.requestPermission();
      if (!hasPermission) return [];

      const songs = await MediaLibrary.getPlaylistAssetsAsync(playlistId);

      return songs.map((song) => ({
        id: song.id,
        title: song.filename,
        artist: song.albumId || 'Unknown',
        album: song.mediaType,
        duration: song.duration || 0,
        uri: song.uri,
        albumArt: undefined,
      }));
    } catch (error) {
      console.error('Failed to fetch playlist songs:', error);
      return [];
    }
  }

  /**
   * Play a specific song from playlist
   */
  async playSong(song: Song): Promise<boolean> {
    try {
      // Stop currently playing song
      if (this.currentSound) {
        await this.currentSound.stopAsync();
        await this.currentSound.unloadAsync();
      }

      // Load and play new song
      const { sound } = await Audio.Sound.createAsync({ uri: song.uri });
      this.currentSound = sound;

      await sound.playAsync();
      this.isPlaying = true;

      return true;
    } catch (error) {
      console.error('Failed to play song:', error);
      return false;
    }
  }

  /**
   * Play entire playlist
   */
  async playPlaylist(playlistId: string, startIndex = 0): Promise<boolean> {
    try {
      const songs = await this.getPlaylistSongs(playlistId);
      if (songs.length === 0) return false;

      this.currentPlaylist = {
        id: playlistId,
        name: playlistId,
        trackCount: songs.length,
        duration: songs.reduce((sum, s) => sum + (s.duration || 0), 0),
      };

      // Play first song
      await this.playSong(songs[startIndex]);

      // Setup queue for subsequent songs
      this.setupPlaylistQueue(songs, startIndex);

      return true;
    } catch (error) {
      console.error('Failed to play playlist:', error);
      return false;
    }
  }

  /**
   * Setup automatic playback of next songs in playlist
   */
  private setupPlaylistQueue(songs: Song[], startIndex: number) {
    if (this.currentSound) {
      this.currentSound.setOnPlaybackStatusUpdate((status) => {
        if (status.isLoaded && status.didJustFinish) {
          // Play next song
          const nextIndex = startIndex + 1;
          if (nextIndex < songs.length) {
            this.playSong(songs[nextIndex]);
            startIndex = nextIndex;
          }
        }
      });
    }
  }

  /**
   * Pause current playback
   */
  async pause(): Promise<boolean> {
    try {
      if (this.currentSound && this.isPlaying) {
        await this.currentSound.pauseAsync();
        this.isPlaying = false;
        return true;
      }
      return false;
    } catch (error) {
      console.error('Failed to pause:', error);
      return false;
    }
  }

  /**
   * Resume playback
   */
  async resume(): Promise<boolean> {
    try {
      if (this.currentSound && !this.isPlaying) {
        await this.currentSound.playAsync();
        this.isPlaying = true;
        return true;
      }
      return false;
    } catch (error) {
      console.error('Failed to resume:', error);
      return false;
    }
  }

  /**
   * Skip to next song
   */
  async skipToNext(): Promise<boolean> {
    // In a real implementation, track current index and load next
    console.log('Skip to next not yet implemented');
    return false;
  }

  /**
   * Set volume (0.0 to 1.0)
   */
  async setVolume(volume: number): Promise<void> {
    try {
      if (this.currentSound) {
        await this.currentSound.setVolumeAsync(Math.max(0, Math.min(1, volume)));
      }
    } catch (error) {
      console.error('Failed to set volume:', error);
    }
  }

  /**
   * Stop playback and cleanup
   */
  async stop(): Promise<void> {
    try {
      if (this.currentSound) {
        await this.currentSound.stopAsync();
        await this.currentSound.unloadAsync();
        this.currentSound = null;
        this.isPlaying = false;
      }
    } catch (error) {
      console.error('Failed to stop:', error);
    }
  }

  /**
   * Get current playback status
   */
  async getStatus(): Promise<any> {
    if (this.currentSound) {
      return await this.currentSound.getStatusAsync();
    }
    return null;
  }

  /**
   * Save favorite playlist for quick access
   */
  async saveFavoritePlaylist(playlist: LocalPlaylist) {
    try {
      const favorites = await AsyncStorage.getItem('favorite_playlists');
      const playlistsArray = favorites ? JSON.parse(favorites) : [];

      const filtered = playlistsArray.filter((p: LocalPlaylist) => p.id !== playlist.id);
      const updated = [playlist, ...filtered].slice(0, 10);

      await AsyncStorage.setItem('favorite_playlists', JSON.stringify(updated));
    } catch (error) {
      console.error('Failed to save favorite:', error);
    }
  }

  /**
   * Get favorite playlists
   */
  async getFavoritePlaylists(): Promise<LocalPlaylist[]> {
    try {
      const favorites = await AsyncStorage.getItem('favorite_playlists');
      return favorites ? JSON.parse(favorites) : [];
    } catch (error) {
      console.error('Failed to get favorites:', error);
      return [];
    }
  }

  /**
   * Clear current playlist
   */
  async clearCurrentPlaylist() {
    await this.stop();
    this.currentPlaylist = null;
  }
}

export default new LocalPlaylistService();
