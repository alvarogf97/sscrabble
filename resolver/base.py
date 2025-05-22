"""Base"""

import abc
import typing
from connections import spotify


class BaseResolver(abc.ABC):
    def __init__(self, playlist_url: str, message: str, *_, **__) -> None:
        self.playlist_url = playlist_url
        self.message = message
        self.tracks = spotify.get_playlist_tracks(playlist_url)
        self.message_letters = list(message.replace(' ', '').lower())

    def _commit(self, tracks: typing.List[spotify.Track]):
        """Commits the tracklist to the playlist"""
        spotify.commit_tracks_to_playlist(self.playlist_url, tracks)

    @abc.abstractmethod
    def _resolve(self) -> typing.List[spotify.Track]:
        """Resolve tracklist

        Raises:
            errors.ResolverError: whether the message cannot be resolved.

        Returns:
            typing.List[spotify.Track]: a list containing the spotify
                tracks in the desired order.
        """

    @abc.abstractmethod
    def check(self):
        """Checks if it's posible to compose the message

        Raises:
            errors.NotEnoughLettersError: whether there's not enough
                letters to composse the message.
        """

    def resolve(self, commit: bool = False) -> typing.List[spotify.Track]:
        """Resolve spotify message on playlist.

        Attributes:
            commit (bool): if True. Playlist track will be commited.

        Returns:
            typing.List[spotify.Track]: a list containing the tracks in order
                with the compossed message.
        """
        self.check()
        tracks = self._resolve()
        if commit:
            self._commit(tracks)
        return tracks
