from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils.firebase_client import FirebaseClient
from agent.help_request import HelpRequestService
from agent.knowledge_base import KnowledgeBaseManager
from datetime import datetime
import threading
import time

app = Flask(__name__)
firebase = FirebaseClient()
help_service = HelpRequestService()
kb_manager = KnowledgeBaseManager()


def background_timeout_check():
    """Background thread to periodically check for timed-out requests"""
    while True:
        try:
            time.sleep(3600)  # Check every hour
            print("⏰ Running automatic timeout check...")
            firebase.check_and_timeout_old_requests()
        except Exception as e:
            print(f"⚠️ Error in timeout check: {e}")
            time.sleep(3600)  # Wait an hour before retrying


# Start background timeout checker thread
timeout_thread = threading.Thread(target=background_timeout_check, daemon=True)
timeout_thread.start()
print("✅ Background timeout checker started")

@app.route('/')
def index():
    """Dashboard with summary"""
    all_requests = firebase.get_all_requests()

    stats = {
        'pending': sum(1 for r in all_requests.values() if r['status'] == 'pending'),
        'resolved': sum(1 for r in all_requests.values() if r['status'] == 'resolved'),
        'unresolved': sum(1 for r in all_requests.values() if r['status'] == 'unresolved'),
        'total_kb_entries': len(kb_manager.get_all_learned_answers())
    }

    return render_template('index.html', stats=stats)

@app.route('/pending')
def pending_requests():
    """View all pending help requests"""
    pending = firebase.get_pending_requests()

    # Sort by creation time (newest first)
    sorted_pending = sorted(
        [(k, v) for k, v in pending.items()],
        key=lambda x: x[1]['created_at'],
        reverse=True
    )

    return render_template('pending.html', requests=sorted_pending)

@app.route('/respond/<request_id>', methods=['POST'])
def respond_to_request(request_id):
    """Respond to a specific help request"""
    answer = request.form.get('answer', '').strip()

    if not answer:
        return jsonify({'error': 'Answer cannot be empty'}), 400

    try:
        help_service.respond_to_request(request_id, answer)
        return redirect(url_for('pending_requests'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/history')
def history():
    """View resolved and unresolved requests"""
    all_requests = firebase.get_all_requests()

    # Filter resolved/unresolved
    resolved = [(k, v) for k, v in all_requests.items() if v['status'] == 'resolved']
    unresolved = [(k, v) for k, v in all_requests.items() if v['status'] == 'unresolved']

    # Sort by resolution time
    resolved.sort(key=lambda x: x[1].get('resolved_at', ''), reverse=True)
    unresolved.sort(key=lambda x: x[1].get('resolved_at', ''), reverse=True)

    return render_template('history.html', resolved=resolved, unresolved=unresolved)

@app.route('/knowledge-base')
def knowledge_base():
    """View all learned answers"""
    kb_entries = kb_manager.get_all_learned_answers()

    # Sort by creation time
    sorted_kb = sorted(
        [(k, v) for k, v in kb_entries.items()],
        key=lambda x: x[1]['created_at'],
        reverse=True
    )

    return render_template('knowledge_base.html', kb_entries=sorted_kb)

@app.route('/api/timeout-old-requests', methods=['POST'])
def timeout_old_requests():
    """API endpoint to manually trigger timeout check"""
    firebase.check_and_timeout_old_requests()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)