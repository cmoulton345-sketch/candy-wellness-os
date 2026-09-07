// src/screens/PlaylistPickerScreen.tsx
// Let couples pick from playlists already on their device

import React, { useEffect, useState } from 'react';
import {
  View,
  FlatList,
  TouchableOpacity,
  Text,
  Image,
  ActivityIndicator,
  SafeAreaView,
  Modal,
  StyleSheet,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import localPlaylistService, { LocalPlaylist } from '../services/localPlaylistService';

interface PlaylistPickerScreenProps {
  onSelectPlaylist: (playlist: LocalPlaylist) => void;
  onClose: () => void;
}

export const PlaylistPickerScreen = ({
  onSelectPlaylist,
  onClose,
}: PlaylistPickerScreenProps) => {
  const [playlists, setPlaylists] = useState<LocalPlaylist[]>([]);
  const [favorites, setFavorites] = useState<LocalPlaylist[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlaylist, setSelectedPlaylist] = useState<LocalPlaylist | null>(null);

  useEffect(() => {
    loadPlaylists();
  }, []);

  const loadPlaylists = async () => {
    setLoading(true);
    try {
      const devicePlaylists = await localPlaylistService.getDevicePlaylists();
      const favoritesList = await localPlaylistService.getFavoritePlaylists();

      setPlaylists(devicePlaylists);
      setFavorites(favoritesList);
    } catch (error) {
      console.error('Failed to load playlists:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlaylist = (playlist: LocalPlaylist) => {
    setSelectedPlaylist(playlist);
  };

  const handleConfirmSelection = () => {
    if (selectedPlaylist) {
      localPlaylistService.saveFavoritePlaylist(selectedPlaylist);
      onSelectPlaylist(selectedPlaylist);
      onClose();
    }
  };

  const PlaylistCard = ({ playlist }: { playlist: LocalPlaylist }) => (
    <TouchableOpacity
      style={[
        styles.playlistCard,
        selectedPlaylist?.id === playlist.id && styles.playlistCardSelected,
      ]}
      onPress={() => handleSelectPlaylist(playlist)}
    >
      {/* Placeholder album art */}
      <View style={styles.albumArtPlaceholder}>
        <Text style={styles.albumArtText}>🎵</Text>
      </View>

      <View style={styles.playlistInfo}>
        <Text style={styles.playlistName} numberOfLines={1}>
          {playlist.name}
        </Text>
        <Text style={styles.playlistMeta}>
          {playlist.trackCount} songs
        </Text>
      </View>

      {selectedPlaylist?.id === playlist.id && (
        <View style={styles.checkmark}>
          <Text style={styles.checkmarkText}>✓</Text>
        </View>
      )}
    </TouchableOpacity>
  );

  return (
    <Modal
      visible={true}
      animationType="slide"
      onRequestClose={onClose}
      presentationStyle="formSheet"
    >
      <LinearGradient
        colors={['#0F0814', '#1A0C27', '#28113B']}
        style={styles.container}
      >
        <SafeAreaView style={styles.safeArea}>
          {/* Header */}
          <View style={styles.header}>
            <TouchableOpacity onPress={onClose}>
              <Text style={styles.closeButton}>✕</Text>
            </TouchableOpacity>
            <Text style={styles.headerTitle}>Choose Your Mood</Text>
            <View style={{ width: 30 }} />
          </View>

          {/* Subtitle */}
          <Text style={styles.subtitle}>
            Pick a playlist from your device to set the mood
          </Text>

          {loading ? (
            <View style={styles.centerContainer}>
              <ActivityIndicator size="large" color="#FF2E63" />
            </View>
          ) : (
            <>
              {/* Favorites Section */}
              {favorites.length > 0 && (
                <View style={styles.section}>
                  <Text style={styles.sectionTitle}>Recent</Text>
                  <FlatList
                    data={favorites}
                    renderItem={({ item }) => <PlaylistCard playlist={item} />}
                    keyExtractor={(item) => item.id}
                    scrollEnabled={false}
                  />
                </View>
              )}

              {/* All Playlists Section */}
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>All Playlists</Text>
                <FlatList
                  data={playlists}
                  renderItem={({ item }) => <PlaylistCard playlist={item} />}
                  keyExtractor={(item) => item.id}
                  scrollEnabled={false}
                  ListEmptyComponent={
                    <Text style={styles.emptyText}>
                      No playlists found. Add some to your device first.
                    </Text>
                  }
                />
              </View>
            </>
          )}

          {/* Confirm Button */}
          {selectedPlaylist && (
            <TouchableOpacity
              style={styles.confirmButton}
              onPress={handleConfirmSelection}
            >
              <LinearGradient
                colors={['#FF2E63', '#FF6B9D']}
                style={styles.confirmButtonGradient}
              >
                <Text style={styles.confirmButtonText}>
                  Play "{selectedPlaylist.name}"
                </Text>
              </LinearGradient>
            </TouchableOpacity>
          )}
        </SafeAreaView>
      </LinearGradient>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F0814',
  },
  safeArea: {
    flex: 1,
    paddingHorizontal: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#28113B',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  closeButton: {
    fontSize: 24,
    color: '#FF2E63',
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 14,
    color: '#B0B0B0',
    marginTop: 16,
    marginBottom: 24,
    textAlign: 'center',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  playlistCard: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 12,
    borderRadius: 12,
    backgroundColor: 'rgba(255, 46, 99, 0.05)',
    marginBottom: 10,
    borderWidth: 1.5,
    borderColor: 'transparent',
  },
  playlistCardSelected: {
    borderColor: '#FF2E63',
    backgroundColor: 'rgba(255, 46, 99, 0.1)',
  },
  albumArtPlaceholder: {
    width: 50,
    height: 50,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 46, 99, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  albumArtText: {
    fontSize: 24,
  },
  playlistInfo: {
    flex: 1,
  },
  playlistName: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  playlistMeta: {
    fontSize: 12,
    color: '#9CA3AF',
  },
  checkmark: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#FF2E63',
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmarkText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: 'bold',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    color: '#9CA3AF',
    fontSize: 14,
    textAlign: 'center',
    paddingVertical: 24,
  },
  confirmButton: {
    marginTop: 24,
    marginBottom: 32,
    borderRadius: 12,
    overflow: 'hidden',
  },
  confirmButtonGradient: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  confirmButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
