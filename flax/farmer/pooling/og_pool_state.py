import time

from flax.util.ints import uint64


class OgPoolState:
    difficulty: uint64
    last_partial_submit_timestamp: float

    def __init__(self, difficulty: uint64 = 1, last_partial_submit_timestamp: float = time.time()):
        self.difficulty = difficulty
        self.last_partial_submit_timestamp = last_partial_submit_timestamp
