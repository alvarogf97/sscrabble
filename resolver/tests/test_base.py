import pytest
from unittest.mock import patch, Mock
from resolver import base
from resolver import errors
from connections import spotify


class DummyResolver(base.BaseResolver):

    def check(self):
        pass

    def _resolve(self):
        return [Mock(spec=spotify.Track, id="1")]


@pytest.fixture
def playlist_url():
    return "https://open.spotify.com/playlist/FAKE_ID?si=xyz"


@pytest.fixture
def message():
    return "abc"


@patch("resolver.base.spotify.get_playlist_tracks")
def test_init_sets_attributes(mock_get_tracks, playlist_url, message):
    mock_get_tracks.return_value = [Mock(spec=spotify.Track, name="A")]
    resolver = DummyResolver(playlist_url, message)
    assert resolver.playlist_url == playlist_url
    assert resolver.message == message
    assert resolver.message_letters == list("abc")
    assert resolver.tracks == mock_get_tracks.return_value


@patch("resolver.base.spotify.commit_tracks_to_playlist")
@patch("resolver.base.spotify.get_playlist_tracks")
def test_resolve_with_commit(
    mock_get_tracks, mock_commit_tracks, playlist_url, message
):
    mock_get_tracks.return_value = [Mock(spec=spotify.Track, name="A")]

    resolver = DummyResolver(playlist_url, message)
    result = resolver.resolve(commit=True)

    assert isinstance(result, list)
    assert mock_commit_tracks.called
    assert mock_commit_tracks.call_args[0][0] == playlist_url


@patch("resolver.base.spotify.get_playlist_tracks")
def test_resolve_without_commit(mock_get_tracks, playlist_url, message):
    mock_get_tracks.return_value = [Mock(spec=spotify.Track, name="A")]

    resolver = DummyResolver(playlist_url, message)
    result = resolver.resolve(commit=False)

    assert isinstance(result, list)


@patch("resolver.base.spotify.get_playlist_tracks")
def test_resolve_raises_from_check(mock_get_tracks, playlist_url, message):
    mock_get_tracks.return_value = [Mock(spec=spotify.Track, name="A")]

    class FailingResolver(base.BaseResolver):
        def check(self):
            raise errors.NotEnoughLettersError("Error", missings={})

        def _resolve(self):
            return []

    resolver = FailingResolver(playlist_url, message)

    with pytest.raises(errors.NotEnoughLettersError):
        resolver.resolve()