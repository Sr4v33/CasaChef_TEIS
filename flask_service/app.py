from flask import Flask, request, jsonify
from decimal import Decimal

app = Flask(__name__)

@app.route("/api/v2/payments/", methods=["POST"])
def pay_order():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data"}), 400

        order_id = data.get("order_id")
        amount = data.get("amount")
        method = data.get("method")

        if not order_id or not amount or not method:
            return jsonify({"error": "Datos incompletos"}), 400

        # Simulación del pago
        return jsonify({
            "message": "Pago procesado en Flask",
            "order_id": order_id,
            "amount": amount,
            "method": method,
            "status": "confirmed"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)