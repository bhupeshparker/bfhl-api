from flask import Flask, request, jsonify
import os

app = Flask(__name__)

EMAIL = "bhupesh1807.be23@chitkara.edu.in"

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        data = request.json.get("data", [])

        numbers = [x for x in data if x.isdigit()]
        alphabets = [x for x in data if x.isalpha()]

        return jsonify({
            "is_success": True,
            "official_email": EMAIL,
            "numbers": numbers,
            "alphabets": alphabets
        }), 200

    except Exception:
        return jsonify(is_success=False), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify(is_success=True, official_email=EMAIL), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
