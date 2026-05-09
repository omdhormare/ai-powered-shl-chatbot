from flask import Blueprint, jsonify, request

from app.chat_engine import ChatEngine

api = Blueprint("api", __name__)
engine = ChatEngine()


@api.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id", "default")
    message = payload.get("message", "").strip()

    if not message:
        return jsonify({"error": "'message' is required"}), 400

    try:
        result = engine.reply(session_id=session_id, message=message)
        return jsonify(result), 200
    except Exception as exc:
        return jsonify({"error": "Internal server error", "details": str(exc)}), 500
