import requests
from app.core.config import get_settings
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

# import requests
# from app.core.config import get_settings
# from app.core.exceptions import CustomError
# from app.utils.logger import logger
# import time

# settings = get_settings()


# class RealTimeStockService:
#     BASE_URL = "https://api.twelvedata.com/price"

#     def get_live_price(self, symbol: str):
#         if not symbol or not symbol.strip():
#             raise CustomError("Stock symbol is required")

#         symbol = symbol.upper()

#         if not settings.TWELVEDATA_API_KEY:
#             raise CustomError("Stock API key is not configured on server", 500)

#         params = {
#             "symbol": symbol,
#             "apikey": settings.TWELVEDATA_API_KEY
#         }

#         # ✅ Retry Mechanism (2 attempts)
#         for attempt in range(2):
#             try:
#                 response = requests.get(self.BASE_URL, params=params, timeout=10)
#                 break
#             except requests.RequestException as e:
#                 logger.error(f"Stock API network error (Attempt {attempt+1}): {str(e)}")
#                 time.sleep(1)
#         else:
#             raise CustomError("Stock data provider unreachable")

#         if response.status_code != 200:
#             logger.error(f"Stock API HTTP Error: {response.text}")
#             raise CustomError("Stock provider error")

#         data = response.json()

#         logger.info(f"Live stock response for {symbol}: {data}")

#         # ✅ API-Level Errors (Quota, Symbol, etc.)
#         if "status" in data and data["status"] == "error":
#             raise CustomError(data.get("message", "Invalid stock symbol"))

#         if "code" in data and data.get("code") in [401, 429]:
#             raise CustomError(data.get("message", "Stock API rate limit exceeded"), 429)

#         if "price" not in data:
#             raise CustomError("Invalid stock symbol")

#         return {
#             "symbol": symbol,
#             "price": float(data["price"]),
#             "currency": "USD",   # TwelveData default
#             "source": "Twelve Data (Live Market)",
#             "timestamp": data.get("timestamp"),
#         }
