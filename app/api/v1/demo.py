# app/api/v1/demo.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["demo"])


@router.get("/demo/payment", response_class=HTMLResponse)
async def demo_payment_page():
    # NOTE: Yeh sample hai, isme tum apna actual JS / CSS laga sakte ho.
    html = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>StockPulse Demo Payment</title>
    </head>
    <body>
      <h2>Demo Stock Payment (Mock)</h2>
      <p>Symbol: TCS | Qty: 5 | Price: 3500 | Total: 17500</p>
      <button onclick="initPayment()">Init Payment</button>

      <pre id="result"></pre>

      <script>
        async function initPayment() {
          const res = await fetch('/api/v1/payments/stock-init', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              // Yaha pe Authorization header add karna padega real UI me
            },
            body: JSON.stringify({
              symbol: 'TCS',
              quantity: 5,
              price_per_unit: 3500,
              currency: 'INR'
            })
          });

          const data = await res.json();
          document.getElementById('result').innerText = JSON.stringify(data, null, 2);
        }
      </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
