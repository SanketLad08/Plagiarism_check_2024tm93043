from flask import Flask, request, jsonify, abort
import joblib
from utils import calculate_cosine_similarity, highlight_matching_text

app = Flask(__name__)
model = joblib.load("plagiarism_model.pkl")

# maximum allowed bytes for each uploaded file (1 * 1024): change to 1024 for 1KB if you want to match Kong plugin
MAX_BYTES = 1 * 1024 * 1024  # 1 MB safe default for development

@app.route("/check", methods=["POST"])
def check():
    # pre-check total content length (may be None)
    total_len = request.content_length
    if total_len is not None and total_len > MAX_BYTES * 4:  # very large combined payload
        return jsonify({"error": "payload too large"}), 413

    # required files
    if 'original' not in request.files or 'submission' not in request.files:
        return jsonify({"error": "missing files"}), 400

    f1 = request.files['original']
    f2 = request.files['submission']

    # safe size check per file (use stream to avoid reading huge files)
    f1.stream.seek(0, 2); size1 = f1.stream.tell(); f1.stream.seek(0)
    f2.stream.seek(0, 2); size2 = f2.stream.tell(); f2.stream.seek(0)
    if size1 > MAX_BYTES or size2 > MAX_BYTES:
        return jsonify({"error": "file too large"}), 413

    # read bytes safely, attempt decode if text
    b1 = f1.read()
    b2 = f2.read()

    # try decode; if failure, return a clear error (or you may use errors='replace' to proceed)
    try:
        text1 = b1.decode("utf-8")
        text2 = b2.decode("utf-8")
    except UnicodeDecodeError:
        # treat as too large/invalid encoding for text-based plagiarism check
        return jsonify({"error": "uploaded files are not valid UTF-8 text"}), 415

    similarity = calculate_cosine_similarity(text1, text2)
    prediction = model.predict([[similarity]])[0]
    prob = model.predict_proba([[similarity]])[0][1]

    highlighted1, highlighted2 = highlight_matching_text(text1, text2)

    return jsonify({
        "similarity_score": round(float(similarity), 4),
        "plagiarized": bool(prediction),
        "probability": round(float(prob), 4),
        "highlighted_original": highlighted1,
        "highlighted_submission": highlighted2
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
