import pytest
from unittest.mock import patch, Mock
from connections.spotify import (
    get_playlist_tracks,
    clean_tracks_from_playlist,
    commit_tracks_to_playlist,
    Track,
    SpotifyConnectionError,
)
 

@pytest.fixture
def fake_config():
    return Mock(access_token='fake_token')


@pytest.fixture
def fake_track():
    return Track(id='123', name='Song', artist='Artist')


@pytest.fixture
def playlist_url():
    return 'https://open.spotify.com/playlist/FAKE_ID?si=123'


@patch('connections.spotify.get_config')
@patch('connections.spotify.requests.get')
def test_get_playlist_tracks_success(
    mock_get, mock_config, playlist_url, fake_config
):
    mock_config.return_value = fake_config

    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        'items': [
            {
                'track': {
                    'id': '1',
                    'name': 'Song A',
                    'artists': [{'name': 'Artist A'}],
                }
            },
            {
                'track': {
                    'id': '2',
                    'name': 'Song B',
                    'artists': [{'name': 'Artist B'}],
                }
            },
        ],
        'next': None,
    }

    mock_get.return_value = mock_response

    tracks = get_playlist_tracks(playlist_url)
    assert len(tracks) == 2
    assert tracks[0].name == 'Song A'
    assert tracks[1].artist == 'Artist B'


@patch('connections.spotify.get_config')
@patch('connections.spotify.requests.get')
def test_get_playlist_tracks_error(
    mock_get, mock_config, playlist_url, fake_config
):
    mock_config.return_value = fake_config

    mock_response = Mock()
    mock_response.ok = False
    mock_response.content = b'unauthorized'

    mock_get.return_value = mock_response

    with pytest.raises(SpotifyConnectionError):
        get_playlist_tracks(playlist_url)


@patch('connections.spotify.get_config')
@patch('connections.spotify.requests.delete')
def test_clean_tracks_success(
    mock_delete, mock_config, playlist_url, fake_config, fake_track
):
    mock_config.return_value = fake_config

    mock_response = Mock()
    mock_response.ok = True
    mock_delete.return_value = mock_response

    clean_tracks_from_playlist(playlist_url, [fake_track])
    mock_delete.assert_called_once()


@patch('connections.spotify.get_config')
@patch('connections.spotify.requests.delete')
def test_clean_tracks_error(
    mock_delete, mock_config, playlist_url, fake_config, fake_track
):
    mock_config.return_value = fake_config

    mock_response = Mock()
    mock_response.ok = False
    mock_response.content = b'failed'
    mock_delete.return_value = mock_response

    with pytest.raises(SpotifyConnectionError):
        clean_tracks_from_playlist(playlist_url, [fake_track])


@patch('connections.spotify.clean_tracks_from_playlist')
@patch('connections.spotify.get_config')
@patch('connections.spotify.requests.post')
def test_commit_tracks_success(
    mock_post, mock_config, mock_clean, playlist_url, fake_config, fake_track
):
    mock_config.return_value = fake_config
    mock_response = Mock()
    mock_response.ok = True
    mock_post.return_value = mock_response

    commit_tracks_to_playlist(playlist_url, [fake_track], clean=True)
    mock_post.assert_called_once()
    mock_clean.assert_called_once()


@patch('connections.spotify.clean_tracks_from_playlist')
@patch('connections.spotify.get_config')
@patch('connections.spotify.requests.post')
def test_commit_tracks_error(
    mock_post, mock_config, mock_clean, playlist_url, fake_config, fake_track
):
    mock_config.return_value = fake_config
    mock_response = Mock()
    mock_response.ok = False
    mock_response.content = b'error'
    mock_post.return_value = mock_response

    with pytest.raises(SpotifyConnectionError):
        commit_tracks_to_playlist(playlist_url, [fake_track], clean=False)
