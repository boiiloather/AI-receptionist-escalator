from utils.firebase_client import FirebaseClient
from utils.notification import NotificationService
from agent.knowledge_base import KnowledgeBaseManager

class HelpRequestService:
    def __init__(self):
        self.firebase = FirebaseClient()
        self.notification = NotificationService()
        self.kb = KnowledgeBaseManager()

    def create_request(self, question: str, caller_phone: str) -> str:
        """Create help request and notify supervisor"""
        request_id = self.firebase.create_help_request(question, caller_phone)

        # Notify supervisor
        self.notification.notify_supervisor(request_id, question, caller_phone)

        print(f"🆘 Help request created: {request_id}")
        print(f"   Q: {question}")
        print(f"   Caller: {caller_phone}")

        return request_id

    def respond_to_request(self, request_id: str, answer: str):
        """Supervisor provides answer - update KB and notify customer"""
        # Get original request
        request_data = self.firebase.get_ref(f'help_requests/{request_id}').get()

        if not request_data:
            raise ValueError(f"Request {request_id} not found")

        if request_data['status'] != 'pending':
            print(f"⚠️ Request {request_id} already {request_data['status']}")
            return

        # Update request as resolved
        self.firebase.update_request_with_answer(request_id, answer)

        # Add to knowledge base
        self.kb.add_learned_answer(
            request_data['question'], 
            answer, 
            request_id
        )

        # Simulate text back to customer
        self.notification.text_customer(
            request_data['caller_phone'],
            f"Re: '{request_data['question']}'\n\n{answer}"
        )

        print(f"✅ Request {request_id} resolved and KB updated")