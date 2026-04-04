from flask import Flask, jsonify, render_template

app = Flask(__name__)

programs = {
    "FL": {"name": "Fat Loss", "calorie_factor": 22},
    "MG": {"name": "Muscle Gain", "calorie_factor": 35},
    "BG": {"name": "Beginner", "calorie_factor": 26}
}

@app.route("/")
def index():
    # Render the index template with the programs data
    return render_template("index.html", programs=programs)

@app.route("/programs")
def get_all_programs():
    # Keeping the original API endpoint for compatibility
    return jsonify(programs), 200

@app.route("/client/<program_code>")
def get_client_detail(program_code):
    # Render the detail template for a specific program
    program = programs.get(program_code.upper())
    if not program:
        return "Program not found", 404
    return render_template("client_detail.html", program=program, code=program_code.upper())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
