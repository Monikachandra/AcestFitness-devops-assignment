from flask import Flask, jsonify

app = Flask(__name__)

programs_data = {
    "FL": {"name": "Fat Loss", "calorie_factor": 22},
    "MG": {"name": "Muscle Gain", "calorie_factor": 35},
    "BG": {"name": "Beginner", "calorie_factor": 26}
}

@app.route("/")
def health_check():
    return jsonify({"status": "healthy", "message": "ACEest Fitness & Gym API is up and running!"}), 200

@app.route("/programs")
def get_programs():
    return jsonify(programs_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
