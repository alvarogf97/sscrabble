"""Inline resolver

This algorithm will resolve the orther taking care of the first letter.
"""

import typing
from connections import spotify
from resolver import errors, base
from collections import Counter


class InlineResolver(base.BaseResolver):
    """
    This resolver will try to compose the message inline from up to bottom
    """

    def check(self):
        tracklist_letters = Counter(
            [track.name.lower()[0] for track in self.tracks]
        )
        counter = Counter(self.message_letters) - tracklist_letters
        if counter:
            missings = {k: (v, [1]) for k, v in counter.items()}
            raise errors.NotEnoughLettersError(
                'Missing letters', missings=missings
            )

    def _resolve(self) -> typing.List[spotify.Track]:
        """Resolve tracklist

        Raises:
            errors.ResolverError: whether the message cannot be resolved.

        Returns:
            typing.List[spotify.Track]: a list containing the spotify
                tracks in the desired order.
        """
        required_letters = self.message_letters.copy()
        unused_tracks = []
        used_tracks = [None for _ in range(0, len(required_letters))]

        for track in self.tracks:
            if not any(required_letters):
                unused_tracks.append(track)
                continue

            letter = track.name[0].lower()
            try:
                if (i := required_letters.index(letter)) is not None:
                    used_tracks[i] = track
            except ValueError:
                unused_tracks.append(track)
                continue
            required_letters[i] = None

        return used_tracks + unused_tracks
