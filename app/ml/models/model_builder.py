from typing import List

class SimpleAverageModel:
    def fit(self, series: List[float]) -> None:
        pass  # no-op for average baseline

    def predict(self, window: List[float]) -> float:
        return sum(window) / len(window) if window else 0.0
