import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv('.env.local')

class FirebaseClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        """Initialize Firebase Admin SDK with error handling"""
        try:
            cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
            db_url = os.getenv('FIREBASE_DATABASE_URL')
            
            # Handle relative paths
            if cred_path and not os.path.isabs(cred_path):
                cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), cred_path)

            if not cred_path or not db_url:
                raise ValueError("FIREBASE_CREDENTIALS_PATH and FIREBASE_DATABASE_URL must be set in .env.local")

            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")

            cred = credentials.Certificate(cred_path)
            
            # Check if already initialized
            try:
                firebase_admin.get_app()
                print("⚠️ Firebase app already initialized, using existing instance")
            except ValueError:
                # Not initialized yet, initialize now
                firebase_admin.initialize_app(cred, {
                    'databaseURL': db_url
                })
            
            print("✅ Firebase initialized successfully")
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            raise

    def get_ref(self, path):
        """Get database reference"""
        return db.reference(path)

    def create_help_request(self, question, caller_phone):
        """Create a new help request"""
        requests_ref = self.get_ref('help_requests')
        new_request = requests_ref.push({
            'question': question,
            'caller_phone': caller_phone,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'resolved_at': None,
            'supervisor_answer': None
        })
        return new_request.key

    def get_pending_requests(self):
        """Get all pending help requests"""
        requests_ref = self.get_ref('help_requests')
        all_requests = requests_ref.order_by_child('status').equal_to('pending').get()
        return all_requests or {}

    def get_all_requests(self):
        """Get all help requests with history"""
        requests_ref = self.get_ref('help_requests')
        return requests_ref.get() or {}

    def update_request_with_answer(self, request_id, answer):
        """Mark request as resolved with supervisor answer"""
        request_ref = self.get_ref(f'help_requests/{request_id}')
        request_ref.update({
            'status': 'resolved',
            'supervisor_answer': answer,
            'resolved_at': datetime.utcnow().isoformat()
        })

    def mark_request_unresolved(self, request_id):
        """Mark request as unresolved due to timeout"""
        request_ref = self.get_ref(f'help_requests/{request_id}')
        request_ref.update({
            'status': 'unresolved',
            'resolved_at': datetime.utcnow().isoformat()
        })

    def add_to_knowledge_base(self, question, answer, request_id=None):
        """Add learned Q&A to knowledge base"""
        kb_ref = self.get_ref('knowledge_base')
        kb_ref.push({
            'question': question.lower().strip(),
            'answer': answer,
            'learned_from_request_id': request_id,
            'created_at': datetime.utcnow().isoformat()
        })

    def search_knowledge_base(self, question):
        """Search KB for similar question using simple fuzzy matching.

        Strategy:
        - Normalize text (lowercase, strip, collapse spaces)
        - Exact/substring match
        - Token overlap score (Jaccard) with stopword removal
        - Fallback to difflib ratio
        Returns the best answer above threshold, else None.
        """
        import re
        from difflib import SequenceMatcher

        kb_ref = self.get_ref('knowledge_base')
        all_kb = kb_ref.get() or {}

        def normalize(text: str) -> str:
            text = (text or '').lower().strip()
            text = re.sub(r"[^a-z0-9\s]", " ", text)
            text = re.sub(r"\s+", " ", text)
            return text

        STOPWORDS = {
            'the','a','an','do','does','is','are','what','which','and','or','to','for','of',
            'you','your','we','our','on','in','at','about','including','with','vs','list'
        }

        def tokens(text: str) -> set[str]:
            return {t for t in normalize(text).split() if t and t not in STOPWORDS}

        query_raw = question or ''
        query_norm = normalize(query_raw)
        query_tokens = tokens(query_raw)

        best = (0.0, None)  # (score, answer)

        for _, kb_entry in all_kb.items():
            kb_q_raw = kb_entry.get('question', '')
            kb_a = kb_entry.get('answer')
            kb_q_norm = normalize(kb_q_raw)

            # Exact/substring
            if query_norm == kb_q_norm or query_norm in kb_q_norm or kb_q_norm in query_norm:
                return kb_a

            # Token Jaccard
            qtok = query_tokens
            ktok = tokens(kb_q_raw)
            if qtok and ktok:
                inter = len(qtok & ktok)
                union = len(qtok | ktok)
                jacc = inter / union if union else 0.0
            else:
                jacc = 0.0

            # difflib ratio on normalized strings
            ratio = SequenceMatcher(None, query_norm, kb_q_norm).ratio()

            # Combined score (weighted)
            score = 0.7 * jacc + 0.3 * ratio

            if score > best[0]:
                best = (score, kb_a)

        # Threshold to accept fuzzy match
        return best[1] if best[0] >= 0.35 else None

    def get_all_knowledge_base(self):
        """Get all KB entries"""
        kb_ref = self.get_ref('knowledge_base')
        return kb_ref.get() or {}

    def check_and_timeout_old_requests(self):
        """Auto-timeout requests older than threshold"""
        timeout_hours = int(os.getenv('REQUEST_TIMEOUT_HOURS', 4))
        requests_ref = self.get_ref('help_requests')
        pending = requests_ref.order_by_child('status').equal_to('pending').get() or {}

        timeout_threshold = datetime.utcnow() - timedelta(hours=timeout_hours)

        for req_id, req_data in pending.items():
            created_at = datetime.fromisoformat(req_data['created_at'])
            if created_at < timeout_threshold:
                self.mark_request_unresolved(req_id)
                print(f"⏰ Request {req_id} auto-timed out after {timeout_hours} hours")