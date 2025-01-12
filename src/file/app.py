import tempfile

from flask import Flask, jsonify, request
from flask_cors import CORS

from capa import capa

app = Flask(__name__)
CORS(app)


@app.route("/capa_analyze", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

        capa_results = capa(temp_file_path)

        return capa_results


if __name__ == "__main__":
    app.run(debug=True)
