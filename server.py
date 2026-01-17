"""
Flask server for Explosive Girlfriend AI
Railway-safe version
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

print("🚀 server.py loading...")

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

ai = None  # lazy init


def get_ai():
    global ai
    if ai is None:
        print("🤖 Initializing ExplosiveGirlfriendAI...")
        from girlfriend_ai import ExplosiveGirlfriendAI
        ai = ExplosiveGirlfriendAI()
    return ai


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({'success': False, 'error': 'Missing message'}), 400

        user_input = data['message'].strip()
        if not user_input:
            return jsonify({'success': False, 'error': 'Empty message'}), 400

        ai_instance = get_ai()
        result = ai_instance.chat(user_input)

        return jsonify(result), 200

    except Exception as e:
        print("💥 chat error:", e)
        return jsonify({
            'success': False,
            'error': str(e),
            'response': 'Hmph... server messed up.'
        }), 500


@app.route('/api/status')
def status():
    try:
        return jsonify(get_ai().get_emotion_status()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    try:
        get_ai().reset_conversation()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🌍 Flask starting on port {port}")
    app.run(host="0.0.0.0", port=port)
