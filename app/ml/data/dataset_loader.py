from typing import List
import random

class DatasetLoader:
    def load_prices(self, symbol: str, days: int = 30) -> List[float]:
        # Placeholder: generate synthetic price series
        base = random.uniform(50, 200)
        return [round(base + random.uniform(-2, 2), 2) for _ in range(days)]
