import json

class ChatSetup:
    def __init__(self):
        self.chat_history = []

    def parse_llm_response(self, llm_response):
        return json.loads(llm_response)


    def process_interaction(self, llm_response, user_response):
        parsed_response = self.parse_llm_response(llm_response)
        
        interaction = {
            "question": parsed_response["question"],
            "options": parsed_response["options"],
            "response": user_response
        }
        
        self.chat_history.append(interaction)
        
        return self.chat_history, parsed_response

    def get_last_user_response(self):
        if self.chat_history:
            return self.chat_history[-1]["response"]
        return ""

    def get_formatted_chat_history(self):
        if self.chat_history:
            last_entry = self.chat_history[-1]
            return f"Q: {last_entry['question']}\nA: {last_entry['response']}"
        return ""
