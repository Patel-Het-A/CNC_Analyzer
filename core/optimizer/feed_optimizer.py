import numpy as np
from sklearn.ensemble import GradientBoostingRegressor


class FeedOptimizer:
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3
        )
        self.trained = False

    def train(self):
        #  Dummy dataset (expand later)
        # Features: [depth, segment_length, is_cutting]
        X = np.array([
            [1, 10, 1],
            [2, 20, 1],
            [3, 30, 1],
            [4, 40, 1],
            [5, 50, 1],
            [1, 15, 0],
            [2, 25, 0],
            [3, 35, 0],
        ])

        # Target: feed rate
        y = np.array([
            300, 260, 220, 180, 140,
            400, 380, 360
        ])

        self.model.fit(X, y)
        self.trained = True

    def extract_features(self, segment):
        depth = abs(segment.end.z)

        length = (
            (segment.end.x - segment.start.x) ** 2 +
            (segment.end.y - segment.start.y) ** 2 +
            (segment.end.z - segment.start.z) ** 2
        ) ** 0.5

        is_cutting = 1 if segment.is_cutting else 0

        return [depth, length, is_cutting]

    def optimize(self, toolpath):
        if not self.trained:
            self.train()

        for seg in toolpath:
            features = np.array([self.extract_features(seg)])
            predicted_feed = self.model.predict(features)[0]

            if seg.is_cutting:
                seg.feed = predicted_feed

        return toolpath