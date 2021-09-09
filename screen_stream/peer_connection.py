from aiortc.contrib.media import MediaRelay

from .screen_track import ScreenTrack


def create_local_tracks():
    video_track, relay = ScreenTrack(), MediaRelay()
    return relay.subscribe(video_track)


