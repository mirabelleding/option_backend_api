from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/option_data")
def get_option_data():
    ticker_symbol = request.args.get("ticker")
    try:
        ticker = yf.Ticker(ticker_symbol)
        price = ticker.history(period="1d")["Close"].iloc[-1]
        expiries = ticker.options[:5]

        option_chain = {}

        for expiry in expiries:
            chain = ticker.option_chain(expiry)
            # Convert to dict so it's JSON serializable
            option_chain[expiry] = {
                "calls": chain.calls.to_dict(orient="records"),
                "puts": chain.puts.to_dict(orient="records")
            }

        return jsonify({
            "price": round(price, 2),
            "expires": expiries,
            "option_chain": option_chain,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
