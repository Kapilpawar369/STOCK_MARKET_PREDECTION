import requests
from app.core.config import get_settings
# from app.core.exceptions import BadRequest
from app.core.exceptions import CustomError

settings = get_settings()

class RealTimeStockService:
    BASE_URL = "https://api.twelvedata.com/price"

    def get_live_price(self, symbol: str):
        if not symbol or not symbol.strip():
            raise CustomError("Stock symbol is required")

        symbol = symbol.upper()

        params = {
            "symbol": symbol,
            "apikey": settings.STOCK_API_KEY
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
        except requests.RequestException:
            raise CustomError("Stock data provider unreachable")

        if response.status_code != 200:
            raise CustomError("Stock provider error")

        data = response.json()

        # DEBUG LOG (TEMPORARY)
        print("REAL-TIME API RESPONSE:", data)

        # PROVIDER ERROR HANDLING
        if "status" in data and data["status"] == "error":
            raise CustomError(data.get("message", "Invalid stock symbol"))

        if "price" not in data:
            raise CustomError("Invalid stock symbol")

        return {
            "symbol": symbol,
            "price": float(data["price"]),
            "source": "Twelve Data (Live Market)"
        }
