from chatbot import Chatbot

class ChatbotImplementation(Chatbot):

    def __init__(self):
        Chatbot.__init__(self)

    def get_prompt(self, messages, intent, session_id):

        if intent["name"] == "climate_change_is_a_scientific_fact":
            prompt = """This is a conversation between a user and a climate change denier. The climate change denier is very angry and insults the user. His believs are:

    Climate change is a hoax.
    All members of the green party are stupid.
    All scientists are liars.

"""
            success = True
        else:
            prompt = """This is a conversation between a user and a climate change denier. His believs are:

Climate change is a hoax.
All members of the green party are stupid.
All scientists are liars.

"""
            success = False

        final_prompt = self.build_prompt(prompt, messages)
        return final_prompt, success

