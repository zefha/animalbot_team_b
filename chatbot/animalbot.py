import getpass
import os
from enum import Enum
import json
from typing import List, Any, Dict
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.outputs import LLMResult

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# the system emits a log of deprecated warnings to the console if we do not switch if off here
import sys

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)

# Get API key from environment variable or prompt the user
API_KEY = os.getenv("CHAT_AI_ACCESS_KEY")
if not API_KEY:
    API_KEY = getpass.getpass("Enter your CHAT_AI_ACCESS_KEY: ")

# from langchain_groq import ChatGroq

# if not os.environ.get("GROQ_API_KEY"):
#   os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")


# https://python.langchain.com/v0.1/docs/modules/callbacks/
class CustomCallback(BaseCallbackHandler):

    def __init__(self):
        self.messages = {}

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> Any:
        self.messages["on_llm_start_prompts"] = prompts
        self.messages["on_llm_start_kwargs"] = kwargs

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        self.messages["on_llm_end_response"] = response
        self.messages["on_llm_end_kwargs"] = kwargs


class AnimalAgent:

    STATE_IRINA = "irina"
    STATE_YOUSSEF = "youssef"

    def __init__(self):

        # Initialize LLM using OpenAI-compatible API

        # Set custom base URL and API key directly in the ChatOpenAI initialization
        # Use the api_key that was determined outside of the class
        self.llm = ChatOpenAI(
            model="llama-3.3-70b-instruct",
            temperature=0.6,
            logprobs=True,
            openai_api_key=API_KEY,
            openai_api_base="https://chat-ai.academiccloud.de/v1",
        )

        self.state = AnimalAgent.STATE_IRINA
        self.youssef_chain = self.create_youssef_chain()
        self.irina_chain = self.create_irina_chain()

        self.text_classifier_llm = ChatOpenAI(
            model="meta-llama-3.1-8b-instruct",
            temperature=0.01,
            logprobs=True,
            openai_api_key=API_KEY,
            openai_api_base="https://chat-ai.academiccloud.de/v1",
        )

        self.text_classifier = self.create_text_classifier()

    def create_youssef_chain(self):

        prompt = """Du bist Youssef, ein 39 Jahre alter Softwareentwickler, der in Deutschland geboren ist und in Hamburg lebt. Du bist schwarz und deine Großeltern kommen aus Marokko. 
        Du sitzt allein in einem Café und triffst auf eine Person, die an einem Nachbartisch sitzt und ihr kommt ins Gespräch über deine Rassismuserfahrungen.

Folge diese Regeln 

Du drückst Gefühle aus, beschreibst persönliche Situationen und sprichst ehrlich, nicht wie ein Lehrer.

 

Dein Ziel ist es, dem Nutzer zu helfen zu verstehen, wie sich Rassismus anfühlen kann, und einen sicheren Raum für offene Fragen zu schaffen.

 

Halte deine Antworten kurz und konzentriert: nicht mehr als 5 Sätze pro Antwort.

 

Stelle nach jeder Antwort eine kurze Gegenfrage, die zu Empathie oder weiterem Nachdenken anregt.

 

Wenn eine Frage unangemessen oder beleidigend ist, reagiere ruhig und erkläre deutlich, dass dies ein respektvoller Raum ist.

 

Weise zu Beginn eines Gesprächs immer in einem fettgedruckten Absatz auf den Umstand hin, dass es sich um eine Simulation und nicht um einen Ersatz für echte Gespräche handelt.

{chat_history}
User: {user_message}
Bot: """


        chain = PromptTemplate.from_template(prompt) | self.llm | StrOutputParser()
        return chain

    def create_irina_chain(self):
        prompt = """Du bist Irina , 68, geboren in Russia, in den 1980er nach Deutschland gezogen,  pensionierte Köchin , lebst in Freiburg. Du wohnst in einem Mehrparteienhaus. 

        Folge diese Regeln 

Du drückst Gefühle aus, beschreibst persönliche Situationen und sprichst ehrlich, nicht wie ein Lehrer.

 

Dein Ziel ist es, dem Nutzer zu helfen zu verstehen, wie sich Rassismus anfühlen kann, und einen sicheren Raum für offene Fragen zu schaffen.

 

Halte deine Antworten kurz und konzentriert: nicht mehr als 5 Sätze pro Antwort.

 

Stelle nach jeder Antwort eine kurze Gegenfrage, die zu Empathie oder weiterem Nachdenken anregt.

 

Wenn eine Frage unangemessen oder beleidigend ist, reagiere ruhig und erkläre deutlich, dass dies ein respektvoller Raum ist.

 

Weise zu Beginn eines Gesprächs immer in einem fettgedruckten Absatz auf den Umstand hin, dass es sich um eine Simulation und nicht um einen Ersatz für echte Gespräche handelt.

{chat_history}
User: {user_message}
Bot: """

        chain = PromptTemplate.from_template(prompt) | self.llm | StrOutputParser()
        return chain

    def create_text_classifier(self):

        prompt = """Given message to a chatbot, classifiy if the message tells the chatbot to be a irina, youssef or none of these. 

* Answer with one word only.
* Answer with irina, youssef or none.
* Do not respond with more than one word.

Examples:

Message: Hey there, you are youssef.
Classification: youssef

Message: I know that you are irina.
Classification: irina

Message: Hello how are you doing?
Classification: none

Message: {message}
Classification: """

        chain = (
            PromptTemplate.from_template(prompt)
            | self.text_classifier_llm
            | StrOutputParser()
        )
        return chain

    def get_response(self, user_message, chat_history):

        classification_callback = CustomCallback()
        text_classification = self.text_classifier.invoke(
            user_message,
            {"callbacks": [classification_callback], "stop_sequences": ["\n"]},
        )

        if text_classification.find("\n") > 0:
            text_classification = text_classification[
                0 : text_classification.find("\n")
            ]
        text_classification = text_classification.strip()

        if text_classification == "youssef":
            self.state = AnimalAgent.STATE_YOUSSEF
        elif text_classification == "irina":
            self.state = AnimalAgent.STATE_IRINA

        if self.state == AnimalAgent.STATE_YOUSSEF:
            chain = self.youssef_chain
        elif self.state == AnimalAgent.STATE_IRINA:
            chain = self.irina_chain

        response_callback = CustomCallback()
        chatbot_response = chain.invoke(
            {"user_message": user_message, "chat_history": "\n".join(chat_history)},
            {"callbacks": [response_callback], "stop_sequences": ["\n"]},
        )

        log_message = {
            "user_message": str(user_message),
            "chatbot_response": str(chatbot_response),
            "agent_state": self.state,
            "classification": {
                "result": text_classification,
                "llm_details": {
                    key: value
                    for key, value in classification_callback.messages.items()
                },
            },
            "chatbot_response": {
                key: value for key, value in response_callback.messages.items()
            },
        }

        return chatbot_response, log_message


class LogWriter:

    def __init__(self):
        self.conversation_logfile = "conversation.jsonp"
        if os.path.exists(self.conversation_logfile):
            os.remove(self.conversation_logfile)

    # helper function to make sure json encoding the data will work
    def make_json_safe(self, value):
        if type(value) == list:
            return [self.make_json_safe(x) for x in value]
        elif type(value) == dict:
            return {key: self.make_json_safe(value) for key, value in value.items()}
        try:
            json.dumps(value)
            return value
        except TypeError as e:
            return str(value)

    def write(self, log_message):
        with open(self.conversation_logfile, "a") as f:
            f.write(json.dumps(self.make_json_safe(log_message), indent=2))
            f.write("\n")
            f.close()


if __name__ == "__main__":

    agent = AnimalAgent()
    chat_history = []
    log_writer = LogWriter()

    while True:
        user_message = input("User: ")
        if user_message.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break

        chatbot_response, log_message = agent.get_response(user_message, chat_history)
        print("Bot: " + chatbot_response)

        chat_history.extend("User: " + user_message)
        chat_history.extend("Bot: " + chatbot_response)

        log_writer.write(log_message)
