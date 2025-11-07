from datetime import datetime

class NotificationService:
    def notify_supervisor(self, request_id: str, question: str, caller_phone: str):
        """Notify supervisor of new help request (console for now)"""
        print("\n" + "="*60)
        print("🔔 NEW HELP REQUEST")
        print("="*60)
        print(f"Request ID: {request_id}")
        print(f"Question: {question}")
        print(f"Caller: {caller_phone}")
        print(f"Time: {datetime.utcnow().isoformat()}")
        print(f"Action: Visit http://localhost:5000/pending to respond")
        print("="*60 + "\n")

    def text_customer(self, phone: str, message: str):
        """Simulate text message to customer (console for now)"""
        print("\n" + "-"*60)
        print("📱 SIMULATED TEXT MESSAGE")
        print("-"*60)
        print(f"To: {phone}")
        print(f"Message: {message}")
        print(f"Time: {datetime.utcnow().isoformat()}")
        print("-"*60 + "\n")

        # TODO: Integrate with Twilio for real SMS
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=message,
        #     from_='+1234567890',
        #     to=phone
        # )