// frontend/script.js

const API_BASE_URL = window.location.origin + '/api';

// DOM Elements
const generateForm = document.getElementById('generateForm');
const wordInput = document.getElementById('wordInput');
const languageSelect = document.getElementById('languageSelect');
const generateBtn = document.getElementById('generateBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');

const inputSection = document.getElementById('inputSection');
const playerSection = document.getElementById('playerSection');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

const trackTitle = document.getElementById('trackTitle');
const trackGenre = document.getElementById('trackGenre');
const trackMood = document.getElementById('trackMood');
const trackStyle = document.getElementById('trackStyle');
const trackLanguage = document.getElementById('trackLanguage');
const trackDuration = document.getElementById('trackDuration');
const trackKeyword = document.getElementById('trackKeyword');

const audioPlayer = document.getElementById('audioPlayer');
const lyricsSection = document.getElementById('lyricsSection');
const lyricsContent = document.getElementById('lyricsContent');

const generateNewBtn = document.getElementById('generateNewBtn');

// Playlist elements
const addToPlaylistBtn = document.getElementById('addToPlaylistBtn');
const viewPlaylistsBtn = document.getElementById('viewPlaylistsBtn');
const viewPlaylistsBtnMain = document.getElementById('viewPlaylistsBtnMain');
const playlistModal = document.getElementById('playlistModal');
const closePlaylistModal = document.getElementById('closePlaylistModal');
const playlistSelect = document.getElementById('playlistSelect');
const newPlaylistName = document.getElementById('newPlaylistName');
const newPlaylistGroup = document.getElementById('newPlaylistGroup');
const confirmAddToPlaylist = document.getElementById('confirmAddToPlaylist');
const playlistsSection = document.getElementById('playlistsSection');
const playlistsList = document.getElementById('playlistsList');
const createPlaylistBtn = document.getElementById('createPlaylistBtn');
const playlistViewModal = document.getElementById('playlistViewModal');
const closePlaylistViewModal = document.getElementById('closePlaylistViewModal');
const playlistViewTitle = document.getElementById('playlistViewTitle');
const playlistTracks = document.getElementById('playlistTracks');

// Global variables
let currentTrackId = null;
let playlists = [];
let draggedItem = null; // For drag-and-drop

// Event Listeners
generateForm.addEventListener('submit', handleGenerate);
generateNewBtn.addEventListener('click', resetForm);
addToPlaylistBtn.addEventListener('click', showPlaylistModal);
viewPlaylistsBtnMain.addEventListener('click', showPlaylists);
viewPlaylistsBtn.addEventListener('click', showPlaylists);
closePlaylistModal.addEventListener('click', hidePlaylistModal);
closePlaylistViewModal.addEventListener('click', hidePlaylistViewModal);
confirmAddToPlaylist.addEventListener('click', handleAddToPlaylist);
createPlaylistBtn.addEventListener('click', showCreatePlaylistModal);
playlistSelect.addEventListener('change', toggleNewPlaylistInput);

// Generate Music Handler
async function handleGenerate(e) {
    e.preventDefault();

    const word = wordInput.value.trim();
    const language = languageSelect.value;

    if (!word) {
        showError('Please enter a word or name');
        return;
    }

    try {
        setLoading(true);
        hideError();

        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ word, language })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Failed to generate music');
        }

        if (result.success) {
            displayTrack(result.data, result.trackId);
        } else {
            throw new Error('Generation failed');
        }

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Something went wrong. Please try again.');
    } finally {
        setLoading(false);
    }
}

// Display Track
function displayTrack(data, trackId = null) {
    const { track, metadata } = data;

    // Store current track ID for playlist operations
    currentTrackId = trackId || metadata.keyword;

    // Update track info
    trackTitle.textContent = track.title;
    trackGenre.textContent = track.genre;
    trackMood.textContent = track.mood;
    trackStyle.textContent = track.style;
    trackLanguage.textContent = track.language;
    trackDuration.textContent = track.duration;
    trackKeyword.textContent = metadata.keyword;

    // Set audio source
    audioPlayer.src = track.audio_url;
    audioPlayer.load();

    // Display lyrics if available
    if (track.lyrics) {
        lyricsContent.textContent = track.lyrics;
        lyricsSection.style.display = 'block';
    } else {
        lyricsSection.style.display = 'none';
    }

    // Show player, hide input
    inputSection.style.display = 'none';
    playerSection.style.display = 'block';

    // Scroll to player
    playerSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Reset Form
function resetForm() {
    wordInput.value = '';
    languageSelect.value = 'English';
    inputSection.style.display = 'block';
    playerSection.style.display = 'none';
    audioPlayer.pause();
    audioPlayer.src = '';
    hideError();
}

// Loading State
function setLoading(isLoading) {
    if (isLoading) {
        generateBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        generateBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Error Handling
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Auto-hide error after 5 seconds
function autoHideError() {
    setTimeout(() => {
        if (errorMessage.style.display === 'flex') {
            hideError();
        }
    }, 5000);
}

// Character counter for input
wordInput.addEventListener('input', (e) => {
    const length = e.target.value.length;
    const maxLength = e.target.maxLength;

    if (length >= maxLength) {
        showError(`Maximum ${maxLength} characters reached`);
        autoHideError();
    }
});

// Playlist Functions
async function showPlaylistModal() {
    if (!currentTrackId) {
        showError('No track selected');
        return;
    }

    try {
        // Load playlists
        await loadPlaylists();

        // Show modal
        playlistModal.style.display = 'flex';
    } catch (error) {
        console.error('Error loading playlists:', error);
        showError('Failed to load playlists');
    }
}

function hidePlaylistModal() {
    playlistModal.style.display = 'none';
    playlistSelect.value = '';
    newPlaylistName.value = '';
    newPlaylistGroup.style.display = 'block';
}

function toggleNewPlaylistInput() {
    const selectedValue = playlistSelect.value;
    newPlaylistGroup.style.display = selectedValue === '' ? 'block' : 'none';
}

async function handleAddToPlaylist() {
    if (!currentTrackId) {
        showError('No track selected');
        return;
    }

    const selectedPlaylistId = playlistSelect.value;
    const newName = newPlaylistName.value.trim();

    try {
        let result;

        if (selectedPlaylistId) {
            // Add to existing playlist
            result = await fetch(`${API_BASE_URL}/playlist/${selectedPlaylistId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'add',
                    track_ids: [currentTrackId]
                })
            });
        } else if (newName) {
            // Create new playlist
            result = await fetch(`${API_BASE_URL}/playlists`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: newName,
                    track_ids: [currentTrackId]
                })
            });
        } else {
            showError('Please select a playlist or enter a new playlist name');
            return;
        }

        const data = await result.json();

        if (!result.ok) {
            throw new Error(data.error || 'Failed to add to playlist');
        }

        if (data.success) {
            showError('Track added to playlist successfully!', 'success');
            hidePlaylistModal();
            await loadPlaylists(); // Refresh playlists
        } else {
            throw new Error(data.error || 'Failed to add track');
        }

    } catch (error) {
        console.error('Error adding to playlist:', error);
        showError(error.message || 'Failed to add track to playlist');
    }
}

async function loadPlaylists() {
    try {
        const response = await fetch(`${API_BASE_URL}/playlists`);
        const data = await response.json();

        if (data.success) {
            playlists = data.playlists;

            // Update playlist select dropdown
            playlistSelect.innerHTML = '<option value="">Create New Playlist</option>';
            playlists.forEach(playlist => {
                const option = document.createElement('option');
                option.value = playlist.id;
                option.textContent = `${playlist.name} (${playlist.track_count} tracks)`;
                playlistSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading playlists:', error);
    }
}

async function showPlaylists() {
    try {
        await loadPlaylists();

        // Show playlists section
        playlistsSection.style.display = 'block';
        playlistsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        renderPlaylists();
    } catch (error) {
        console.error('Error showing playlists:', error);
        showError('Failed to load playlists');
    }
}

function renderPlaylists() {
    playlistsList.innerHTML = '';

    if (playlists.length === 0) {
        playlistsList.innerHTML = '<p class="no-playlists">No playlists yet. Create your first playlist!</p>';
        return;
    }

    playlists.forEach(playlist => {
        const playlistItem = document.createElement('div');
        playlistItem.className = 'playlist-item';
        playlistItem.innerHTML = `
            <div class="playlist-info">
                <h3>${playlist.name}</h3>
                <p>${playlist.track_count} tracks</p>
                <p class="playlist-date">Created: ${new Date(playlist.created_at * 1000).toLocaleDateString()}</p>
            </div>
            <div class="playlist-actions">
                <button class="btn-small" onclick="viewPlaylist('${playlist.id}')">View</button>
                <button class="btn-small" onclick="editPlaylistName('${playlist.id}', '${playlist.name}')">Edit</button>
                <button class="btn-small delete" onclick="deletePlaylist('${playlist.id}')">Delete</button>
            </div>
        `;
        playlistsList.appendChild(playlistItem);
    });
}

async function viewPlaylist(playlistId) {
    try {
        const response = await fetch(`${API_BASE_URL}/playlist/${playlistId}`);
        const data = await response.json();

        if (data.success) {
            const playlist = data.data;
            playlistViewTitle.textContent = playlist.name;

            // Render tracks
            playlistTracks.innerHTML = '';
            if (playlist.tracks_data.length === 0) {
                playlistTracks.innerHTML = '<p class="no-tracks">No tracks in this playlist yet.</p>';
            } else {
                playlist.tracks_data.forEach(trackData => {
                    const trackItem = document.createElement('div');
                    trackItem.className = 'playlist-track-item';
                    trackItem.draggable = true;
                    trackItem.dataset.trackId = trackData.id;
                    trackItem.addEventListener('dragstart', handleDragStart);
                    trackItem.addEventListener('dragover', handleDragOver);
                    trackItem.addEventListener('drop', handleDrop);
                    trackItem.innerHTML = `
                        <div class="track-info">
                            <h4>${trackData.track.title}</h4>
                            <p>${trackData.track.genre} • ${trackData.track.mood}</p>
                            <p class="track-keyword">Keyword: ${trackData.metadata.keyword}</p>
                        </div>
                        <div class="track-actions">
                            <button class="btn-small" onclick="playTrackFromPlaylist('${trackData.id}')">Play</button>
                            <button class="btn-small remove" onclick="removeFromPlaylist('${playlistId}', '${trackData.id}')">Remove</button>
                        </div>
                    `;
                    playlistTracks.appendChild(trackItem);
                });
            }

            playlistViewModal.style.display = 'flex';
            playlistViewModal.dataset.playlistId = playlistId; // Store playlistId for reordering
        } else {
            throw new Error(data.error || 'Failed to load playlist');
        }
    } catch (error) {
        console.error('Error viewing playlist:', error);
        showError('Failed to load playlist');
    }
}

// --- Drag and Drop Handlers ---
function handleDragStart(e) {
    draggedItem = this;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
    this.classList.add('dragging');
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drag-over');
    return false;
}

function handleDrop(e) {
    e.stopPropagation(); // stops the browser from redirecting.
    this.classList.remove('drag-over');

    if (draggedItem !== this) {
        // Swap the HTML content
        draggedItem.innerHTML = this.innerHTML;
        this.innerHTML = e.dataTransfer.getData('text/html');

        // Swap the data-track-id attributes
        const draggedId = draggedItem.dataset.trackId;
        draggedItem.dataset.trackId = this.dataset.trackId;
        this.dataset.trackId = draggedId;
    }

    // Clean up dragging class from all items
    document.querySelectorAll('.playlist-track-item').forEach(item => item.classList.remove('dragging'));

    // Get the new order of track IDs
    const newOrder = Array.from(playlistTracks.children).map(item => item.dataset.trackId);
    const playlistId = playlistViewModal.dataset.playlistId;

    // Send the new order to the backend
    updatePlaylistOrder(playlistId, newOrder);

    return false;
}

async function updatePlaylistOrder(playlistId, ordered_track_ids) {
    try {
        const response = await fetch(`${API_BASE_URL}/playlist/${playlistId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'reorder',
                ordered_track_ids
            })
        });
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Failed to reorder playlist');
        }
        showError('Playlist order updated!', 'success');
    } catch (error) {
        console.error('Error updating playlist order:', error);
        showError(error.message || 'Failed to save new order');
    }
}

async function editPlaylistName(playlistId, currentName) {
    const newName = prompt('Enter the new playlist name:', currentName);

    if (newName === null || newName.trim() === '' || newName.trim() === currentName) {
        // User cancelled, entered nothing, or didn't change the name
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/playlist/${playlistId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'rename',
                name: newName.trim()
            })
        });

        const data = await response.json();

        if (data.success) {
            showError('Playlist renamed successfully!', 'success');
            await loadPlaylists();
            renderPlaylists();
        } else {
            throw new Error(data.error || 'Failed to rename playlist');
        }
    } catch (error) {
        console.error('Error renaming playlist:', error);
        showError(error.message || 'Failed to rename playlist');
    }
}

function hidePlaylistViewModal() {
    playlistViewModal.style.display = 'none';
}

async function deletePlaylist(playlistId) {
    if (!confirm('Are you sure you want to delete this playlist?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/playlist/${playlistId}`, {
            method: 'DELETE'
        });
        const data = await response.json();

        if (data.success) {
            showError('Playlist deleted successfully!', 'success');
            await loadPlaylists();
            renderPlaylists();
        } else {
            throw new Error(data.error || 'Failed to delete playlist');
        }
    } catch (error) {
        console.error('Error deleting playlist:', error);
        showError(error.message || 'Failed to delete playlist');
    }
}

async function removeFromPlaylist(playlistId, trackId) {
    try {
        const response = await fetch(`${API_BASE_URL}/playlist/${playlistId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'remove',
                track_ids: [trackId]
            })
        });
        const data = await response.json();

        if (data.success) {
            showError('Track removed from playlist!', 'success');
            viewPlaylist(playlistId); // Refresh playlist view
        } else {
            throw new Error(data.error || 'Failed to remove track');
        }
    } catch (error) {
        console.error('Error removing track:', error);
        showError(error.message || 'Failed to remove track');
    }
}

function showCreatePlaylistModal() {
    playlistSelect.value = '';
    newPlaylistName.value = '';
    newPlaylistGroup.style.display = 'block';
    playlistModal.style.display = 'flex';
    newPlaylistName.focus();
}

async function playTrackFromPlaylist(trackId) {
    try {
        setLoading(true);
        hideError();

        const response = await fetch(`${API_BASE_URL}/track/${trackId}`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Failed to load track');
        }

        if (result.success) {
            displayTrack(result.data, trackId);
            hidePlaylistViewModal();
        } else {
            throw new Error('Generation failed');
        }

    } catch (error) {
        console.error('Error playing track:', error);
        showError(error.message || 'Failed to play track');
    } finally {
        setLoading(false);
    }
}

// Update error function to handle success messages
function showError(message, type = 'error') {
    errorText.textContent = message;
    errorMessage.className = type === 'success' ? 'success-message' : 'error-message';
    errorMessage.style.display = 'flex';

    if (type === 'success') {
        setTimeout(() => {
            hideError();
        }, 3000);
    }
}