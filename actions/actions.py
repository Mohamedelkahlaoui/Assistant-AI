# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import openai

class ActionResetPassword(Action):

    def name(self) -> str:
        return "action_reset_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_email = tracker.get_slot('email')
        
        if user_email:
            # Example API call (replace with your actual logic)
            response = requests.post('http://example.com/api/reset-password', json={'email': user_email})
            
            if response.status_code == 200:
                dispatcher.utter_message(text="Password reset link has been sent to your email.")
            else:
                dispatcher.utter_message(text="Failed to send reset link. Please try again later.")
        else:
            dispatcher.utter_message(text="Please provide your email address.")

        return []
    
class ActionChatGPT(Action):
    def name(self) -> str:
        return "action_chatgpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Get the latest user message
        user_message = tracker.latest_message.get('text')
        
        # Call the OpenAI API
        openai.api_key = 'your_openai_api_key'
        response = openai.Completion.create(
            engine="text-davinci-003", # or another model
            prompt=user_message,
            max_tokens=150
        )
        
        # Extract the response text
        response_text = response.choices[0].text.strip()
        
        # Send the response back to the user
        dispatcher.utter_message(text=response_text)
        
        return []


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
