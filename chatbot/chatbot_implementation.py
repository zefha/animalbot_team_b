from chatbot import animalbot


class ChatbotImplementation(animalbot):

    def __init__(self):
        animalbot.__init__(self)

    def get_prompt(self, messages, intent, session_id):
        # TODO implement build_prompt method in animalbot
        final_prompt = self.build_prompt(prompt, messages)
        return final_prompt, success
