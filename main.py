from flask import Flask, request, jsonify
import math
import requests
import os

app = Flask(__name__)
EMAIL = "bhupesh1807.be23@chitkara.edu.in"  
GEMINI_KEY = os.getenv("GEMINI_KEY")

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        data = request.json
        if not data or len(data) != 1:
            return jsonify(is_success=False), 400

        if "fibonacci" in data:
            n = data["fibonacci"]
            fib = [0,1]
            for i in range(2, n):
                fib.append(fib[i-1]+fib[i-2])
            return jsonify(is_success=True, official_email=EMAIL, data=fib[:n])

        if "prime" in data:
            primes=[]
            for x in data["prime"]:
                if x > 1 and all(x%i!=0 for i in range(2,int(math.sqrt(x))+1)):
                    primes.append(x)
            return jsonify(is_success=True, official_email=EMAIL, data=primes)

        if "lcm" in data:
            res = data["lcm"][0]
            for x in data["lcm"][1:]:
                res = res*x//gcd(res,x)
            return jsonify(is_success=True, official_email=EMAIL, data=res)

        if "hcf" in data:
            res = data["hcf"][0]
            for x in data["hcf"][1:]:
                res = gcd(res,x)
            return jsonify(is_success=True, official_email=EMAIL, data=res)

        if "AI" in data:
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}",
                json={"contents":[{"parts":[{"text":data['AI']}]}]}
            )
            ans = r.json()["candidates"][0]["content"]["parts"][0]["text"].split()[0]
            return jsonify(is_success=True, official_email=EMAIL, data=ans)

        return jsonify(is_success=False), 400
    except:
        return jsonify(is_success=False), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify(is_success=True, official_email=EMAIL)

@app.route("/bfhl", methods=["POST"])
def bfhl():
    data = request.json.get("data", [])

    numbers = [x for x in data if x.isdigit()]
    alphabets = [x for x in data if x.isalpha()]

    return jsonify({
        "is_success": True,
        "numbers": numbers,
        "alphabets": alphabets
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
