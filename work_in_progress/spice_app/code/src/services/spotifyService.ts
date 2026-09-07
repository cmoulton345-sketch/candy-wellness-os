// src/services/spotifyService.ts
// Spotify OAuth & Playlist Integration

import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';

const SPOTIFY_CLIENT_ID = process.env.EXPO_PUBLIC_SPOTIFY_CLIENT_ID;
const SPOTIFY_REDIRECT_URI = 'com.spiceapp://auth/spotify';
const SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize';
const SPOTIFY_API_BASE = 'https://api.spotify.com/v1';

export interface SpotifyPlaylist {
  id: string;
  name: string;
  description: string;
  imageUrl: string;
  trackCount: number;
  owner: string;
  uri: string;
}

export interface SpotifyUser {
  id: string;
  displayName: string;
  profileImage: string;
}

class SpotifyService {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  /**
   * Initialize Spotify OAuth flow
   */
  async initiateOAuth() {
    const state = Math.random().toString(36).substring(7);
    const scopes = [
      'playlist-read-private',
      'playlist-read-collaborative',
      'streaming',
      'user-read-private',
    ].join('%20');

    const authUrl = `${SPOTIFY_AUTH_URL}?client_id=${SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri=${encodeURIComponent(SPOTIFY_REDIRECT_URI)}&scope=${scopes}&state=${state}`;

    // In a real app, this would open a browser or webview
    console.log('Opening Spotify auth:', authUrl);
    return authUrl;
  }

  /**
   * Exchange auth code for access token
   */
  async exchangeCodeForToken(code: string) {
    try {
      const response = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          client_id: SPOTIFY_CLIENT_ID!,
          grant_type: 'authorization_code',
          code,
          redirect_uri: SPOTIFY_REDIRECT_URI,
        }).toString(),
      });

      const data = await response.json();

      if (data.access_token) {
        this.accessToken = data.access_token;
        this.refreshToken = data.refresh_token;

        // Store securely
        await SecureStore.setItemAsync('spotify_access_token', data.access_token);
        await SecureStore.setItemAsync('spotify_refresh_token', data.refresh_token || '');
        await AsyncStorage.setItem('spotify_token_expiry', 
          Date.now() + (data.expires_in * 1000));

        return true;
      }
    } catch (error) {
      console.error('Spotify token exchange failed:', error);
      return false;
    }
  }

  /**
   * Refresh expired access token
   */
  async refreshAccessToken() {
    try {
      if (!this.refreshToken) {
        this.refreshToken = await SecureStore.getItemAsync('spotify_refresh_token');
      }

      const response = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          client_id: SPOTIFY_CLIENT_ID!,
          grant_type: 'refresh_token',
          refresh_token: this.refreshToken!,
        }).toString(),
      });

      const data = await response.json();

      if (data.access_token) {
        this.accessToken = data.access_token;
        await SecureStore.setItemAsync('spotify_access_token', data.access_token);
        return true;
      }
    } catch (error) {
      console.error('Spotify token refresh failed:', error);
      return false;
    }
  }

  /**
   * Check if token is expired and refresh if needed
   */
  private async ensureValidToken() {
    if (!this.accessToken) {
      this.accessToken = await SecureStore.getItemAsync('spotify_access_token');
    }

    const expiry = await AsyncStorage.getItem('spotify_token_expiry');
    if (expiry && Date.now() > parseInt(expiry)) {
      await this.refreshAccessToken();
    }

    return this.accessToken;
  }

  /**
   * Get user's playlists
   */
  async getUserPlaylists(limit = 50): Promise<SpotifyPlaylist[]> {
    try {
      const token = await this.ensureValidToken();
      if (!token) throw new Error('No Spotify token');

      const response = await fetch(
        `${SPOTIFY_API_BASE}/me/playlists?limit=${limit}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const data = await response.json();

      return data.items.map((playlist: any) => ({
        id: playlist.id,
        name: playlist.name,
        description: playlist.description || '',
        imageUrl: playlist.images[0]?.url || '',
        trackCount: playlist.tracks.total,
        owner: playlist.owner.display_name,
        uri: playlist.uri,
      }));
    } catch (error) {
      console.error('Failed to fetch playlists:', error);
      return [];
    }
  }

  /**
   * Search for playlists (public)
   */
  async searchPlaylists(query: string, limit = 20): Promise<SpotifyPlaylist[]> {
    try {
      const token = await this.ensureValidToken();
      if (!token) throw new Error('No Spotify token');

      const response = await fetch(
        `${SPOTIFY_API_BASE}/search?q=${encodeURIComponent(query)}&type=playlist&limit=${limit}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const data = await response.json();

      return data.playlists.items.map((playlist: any) => ({
        id: playlist.id,
        name: playlist.name,
        description: playlist.description || '',
        imageUrl: playlist.images[0]?.url || '',
        trackCount: playlist.tracks.total,
        owner: playlist.owner.display_name,
        uri: playlist.uri,
      }));
    } catch (error) {
      console.error('Failed to search playlists:', error);
      return [];
    }
  }

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<SpotifyUser | null> {
    try {
      const token = await this.ensureValidToken();
      if (!token) throw new Error('No Spotify token');

      const response = await fetch(
        `${SPOTIFY_API_BASE}/me`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const data = await response.json();

      return {
        id: data.id,
        displayName: data.display_name,
        profileImage: data.images[0]?.url || '',
      };
    } catch (error) {
      console.error('Failed to fetch user:', error);
      return null;
    }
  }

  /**
   * Logout & clear tokens
   */
  async logout() {
    this.accessToken = null;
    this.refreshToken = null;
    await SecureStore.deleteItemAsync('spotify_access_token');
    await SecureStore.deleteItemAsync('spotify_refresh_token');
    await AsyncStorage.removeItem('spotify_token_expiry');
  }

  /**
   * Check if user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    const token = await SecureStore.getItemAsync('spotify_access_token');
    return !!token;
  }

  /**
   * Save recently used playlist for quick access
   */
  async saveRecentPlaylist(playlist: SpotifyPlaylist) {
    try {
      const recents = await AsyncStorage.getItem('spotify_recent_playlists');
      const playlistsArray = recents ? JSON.parse(recents) : [];

      // Remove if already in list
      const filtered = playlistsArray.filter((p: SpotifyPlaylist) => p.id !== playlist.id);

      // Add to front and keep only 5 most recent
      const updated = [playlist, ...filtered].slice(0, 5);

      await AsyncStorage.setItem('spotify_recent_playlists', JSON.stringify(updated));
    } catch (error) {
      console.error('Failed to save recent playlist:', error);
    }
  }

  /**
   * Get recently used playlists
   */
  async getRecentPlaylists(): Promise<SpotifyPlaylist[]> {
    try {
      const recents = await AsyncStorage.getItem('spotify_recent_playlists');
      return recents ? JSON.parse(recents) : [];
    } catch (error) {
      console.error('Failed to get recent playlists:', error);
      return [];
    }
  }
}

export default new SpotifyService();
