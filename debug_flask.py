from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is working!"

@app.route("/debug_routes")
def debug_routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"{rule} -> {rule.endpoint}")
    return "<br>".join(output)

if __name__ == "__main__":
    app.run(debug=True)
