from datetime import datetime, timezone
import threading
import webbrowser
from uuid import uuid4

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from backend.detector import analyze_text, analyze_batch, backend_metadata
from backend.validation import (
    ValidationError,
    validate_payload,
    validate_text,
    validate_input_type,
    MAX_BATCH_ITEMS,
    MAX_TEXT_LENGTH,
)

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
    static_url_path="/static",
)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store" if request.path.startswith("/api/") else "no-cache"
    return response


@app.errorhandler(RequestEntityTooLarge)
def too_large(_):
    return jsonify({
        "error": "Request is too large.",
        "max_request_bytes": app.config["MAX_CONTENT_LENGTH"],
    }), 413


@app.errorhandler(404)
def not_found(_):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found."}), 404
    return render_template("index.html", error="Page not found."), 404


@app.errorhandler(Exception)
def unhandled(exc):
    if request.path.startswith("/api/"):
        return jsonify({
            "error": "Internal server error.",
            "request_id": getattr(request, "request_id", None),
        }), 500
    raise exc


@app.before_request
def attach_request_id():
    request.request_id = uuid4().hex[:12]


@app.after_request
def add_request_id(response):
    response.headers["X-Request-ID"] = request.request_id
    return response


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    content = request.form.get("content", "")
    input_type = request.form.get("input_type", "message")
    try:
        result = analyze_text(content, input_type)
        return render_template("result.html", result=result, text=content)
    except ValidationError as exc:
        return render_template(
            "index.html", error=str(exc), previous=content
        ), 400


@app.post("/api/analyze")
def api_analyze():
    payload = request.get_json(silent=True) or {}
    try:
        content, input_type = validate_payload(payload)
        result = analyze_text(content, input_type)
        return jsonify({
            "success": True,
            "request_id": request.request_id,
            "result": result,
        })
    except ValidationError as exc:
        return jsonify({
            "success": False,
            "request_id": request.request_id,
            "error": str(exc),
        }), 400


@app.post("/api/analyze/batch")
def api_analyze_batch():
    payload = request.get_json(silent=True) or {}
    items = payload.get("items") if isinstance(payload, dict) else None

    if not isinstance(items, list):
        return jsonify({
            "success": False,
            "error": "items must be a JSON array.",
        }), 400

    if not items:
        return jsonify({
            "success": False,
            "error": "items cannot be empty.",
        }), 400

    if len(items) > MAX_BATCH_ITEMS:
        return jsonify({
            "success": False,
            "error": f"Maximum batch size is {MAX_BATCH_ITEMS}.",
        }), 400

    try:
        results = analyze_batch(items)
        return jsonify({
            "success": True,
            "request_id": request.request_id,
            "count": len(results),
            "results": results,
        })
    except (ValidationError, ValueError) as exc:
        return jsonify({
            "success": False,
            "request_id": request.request_id,
            "error": str(exc),
        }), 400


@app.get("/api/health")
def api_health():
    return jsonify({
        "status": "ok",
        "service": "ScamShield",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request.request_id,
    })


@app.get("/health")
def health():
    return api_health()


@app.get("/api/model")
def api_model():
    return jsonify({
        "success": True,
        "metadata": backend_metadata(),
    })


@app.get("/api/scam-types")
def scam_types():
    meta = backend_metadata()
    return jsonify({"success": True, "scam_types": meta["scam_types"]})


@app.get("/api/stages")
def stages():
    meta = backend_metadata()
    return jsonify({"success": True, "stages": meta["stages"]})


@app.get("/history")
def history():
    return render_template("history.html")


@app.get("/analytics")
def analytics():
    return render_template("analytics.html")


@app.get("/guide")
def guide():
    return render_template("guide.html")


@app.get("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"

    # Open the browser shortly after Flask starts. The reloader remains disabled
    # so this also works in Windows IDE/embedded-console environments.
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()

    print("=" * 60)
    print("ScamShield is starting...")
    print(f"Open: {url}")
    print("Press CTRL+C to stop the server.")
    print("=" * 60)

    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
