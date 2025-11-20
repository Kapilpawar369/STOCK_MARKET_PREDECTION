from typing import List

def last_n_days(prices: List[float], n: int = 5) -> List[float]:
    return prices[-n:] if len(prices) >= n else prices
