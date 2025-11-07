from utils.firebase_client import FirebaseClient

class KnowledgeBaseManager:
    def __init__(self):
        self.firebase = FirebaseClient()

    def check_knowledge(self, question: str) -> str | None:
        """Check if we have an answer in KB"""
        return self.firebase.search_knowledge_base(question)

    def add_learned_answer(self, question: str, answer: str, request_id: str = None):
        """Store new learned Q&A"""
        self.firebase.add_to_knowledge_base(question, answer, request_id)
        print(f"📚 Added to KB: Q='{question[:50]}...' A='{answer[:50]}...'")

    def get_all_learned_answers(self):
        """Get all KB entries for display"""
        return self.firebase.get_all_knowledge_base()