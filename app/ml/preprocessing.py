from typing import List

def clean_prices(prices: List[float]) -> List[float]:
    # Remove negatives, fill missing with last value
    cleaned = [max(p, 0.01) for p in prices]
    return cleaned
