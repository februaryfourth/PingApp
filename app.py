from flask import Flask, render_template, jsonify
import subprocess
import re
import json

app = Flask(__name__)

# Load buildings & hostnames
with open("buildings.json", "r") as f:
    buildings = json.load(f)

def ping_host(host):
    """Ping a host and return the status."""
    try:
        result = subprocess.run(["ping", "-n", "1", host], capture_output=True, text=True, timeout=10)
        match = re.search(r"Received = (\d+)", result.stdout)
        received = int(match.group(1)) if match else 0

        if received == 1:
            return "active"
        elif received == 0:
            return "not-active"
        else:
            return "unknown"
    except Exception:
        return "error"

@app.route("/")
def home():
    return render_template("index.html", buildings=buildings.keys())

@app.route("/building/<name>")
def building(name):
    if name not in buildings:
        return "Building not found", 404
    return render_template("building.html", building=name, hostnames=buildings[name])

@app.route("/ping/<building>")
def ping_building(building):
    if building not in buildings:
        return jsonify({"error": "Building not found"}), 404
    
    results = {host: ping_host(host) for host in buildings[building]}
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
