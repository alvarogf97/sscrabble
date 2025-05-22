"""Spotify connection methods"""

import requests
import typing
import pydantic
from tools.config import get_config


_GET_PLAYLIST_TRACKS_URL = (
    'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
)
_CLEAN_PLAYLIST_URL = (
    'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
)
_ADD_TRACKS_PLAYLIST_URL = (
    'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
)


class Track(pydantic.BaseModel):
    id: str
    name: str
    artist: str


class SpotifyConnectionError(Exception):
    """Error raised whether spotify connection cannot be stabilished"""


def get_playlist_tracks(playlist_url: str) -> typing.List[Track]:
    """Retrieve playlist tracks.

    Args:
        playlist_url (str): the playlist url

    Raises:
        SpotifyConnectionError: whether spotify requests goes wrong or there
            there's no acces token available.

    Returns:
        typing.List[Track]: a list containing every playlist track.
    """
    playlist_id = playlist_url.split('/playlist/')[1].split('?')[0]
    url = _GET_PLAYLIST_TRACKS_URL.format(playlist_id=playlist_id)

    headers = {'Authorization': f'Bearer {get_config().access_token}'}

    tracks = []
    while url:
        response = requests.get(url, headers=headers)

        if not response.ok:
            raise SpotifyConnectionError(
                f'Error retrieveing playlist tracks {response.content}'
            )

        try:
            data = response.json()
            for item in data['items']:
                track = item['track']
                if track:
                    name = track['name']
                    artist = ', '.join([a['name'] for a in track['artists']])
                    tracks.append(
                        Track(id=track['id'], name=name, artist=artist)
                    )
            url = data.get('next')
        except requests.JSONDecodeError as err:
            raise SpotifyConnectionError(
                f'Error deserializing tracks {response.content} {err}'
            )
        except KeyError as err:
            raise SpotifyConnectionError(
                f'Unexpected not found key deserializing tracks {err}'
            )

    return tracks


def clean_tracks_from_playlist(playlist_url: str, tracks: typing.List[Track]):
    """Remove the given tracks from the given playlist.

    Args:
        playlist_url (str): the playlist we want remove the tracks from
        tracks (typing.List[Track]): the tracks we want to remove from the
            playlist

    Raises:
        SpotifyConnectionError: whether there's a problem connecting spotify
    """
    playlist_id = playlist_url.split('/playlist/')[1].split('?')[0]
    url = _CLEAN_PLAYLIST_URL.format(playlist_id=playlist_id)
    headers = {'Authorization': f'Bearer {get_config().access_token}'}

    response = requests.delete(
        url,
        headers=headers,
        json={
            'tracks': [{'uri': f'spotify:track:{track.id}'} for track in tracks]
        },
    )

    if not response.ok:
        raise SpotifyConnectionError(
            f'Cannot clean spotify playlist {response.content}'
        )


def commit_tracks_to_playlist(
    playlist_url: str,
    tracks: typing.List[Track],
    clean: bool = True,
    batch_size: int = 100,
):
    """Commit the given tracklist to the playlist.

    Args:
        playlist_url (str): the playlist we want the tracks to be added.
        tracks (typing.List[Track]): the tracks we want add to the playlist.
        clean (bool, optional): If true the given playlist will be cleaned
            before commiting. Defaults to True.
        batch_size (int, optional): batch size. Defaults to 100.

    Raises:
        SpotifyConnectionError: whether there's a problem connecting spotify
    """
    if clean:
        clean_tracks_from_playlist(playlist_url, tracks)

    playlist_id = playlist_url.split('/playlist/')[1].split('?')[0]
    url = _ADD_TRACKS_PLAYLIST_URL.format(playlist_id=playlist_id)
    headers = {'Authorization': f'Bearer {get_config().access_token}'}

    for i in range(0, len(tracks), batch_size):
        batch = [
            f'spotify:track:{track.id}' for track in tracks[i : i + batch_size]
        ]
        response = requests.post(url, headers=headers, json={'uris': batch})
        if not response.ok:
            raise SpotifyConnectionError(
                f'Error commiting to playlist {response.content}'
            )
