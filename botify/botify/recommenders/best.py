from .recommender import Recommender
import random

from botify.recommenders.toppop import TopPop


class Best(Recommender):
    """
    Legendary recommender, superior to every other.
    """

    def __init__(self, tracks_redis, catalog, first_songs):
        self.tracks_redis = tracks_redis
        self.fallback = TopPop(tracks_redis, catalog.top_tracks[:100])
        self.catalog = catalog
        self.first_songs = first_songs

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        # Get first song oin the session
        first_track = self.first_songs[user]

        # Look for it in redis
        first_track_redis = self.tracks_redis.get(first_track)
        if first_track_redis is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        # Get recommendations
        first_track_catalog = self.catalog.from_bytes(first_track_redis)
        recommendations = first_track_catalog.recommendations
        if recommendations is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        return random.choice(list(recommendations))
