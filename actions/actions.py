from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Import functions from your scripts
from Geocoding import get_location_coordinates
from transformers import BertForSequenceClassification, BertTokenizer
import torch
from ilama3_file import generate_ilama3_response

class ActionGeocoding(Action):
    def name(self) -> str:
        return "action_geocoding"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get('text')
        api_key = "AIzaSyCaWAF9DCj2P6d6asrh-b61BNua3zD2gMQ"
        address, latitude, longitude = get_location_coordinates(user_message, api_key)
        if address:
            dispatcher.utter_message(text=f"Location: {address}, Latitude: {latitude}, Longitude: {longitude}")
        else:
            dispatcher.utter_message(text="Failed to retrieve location information.")
        return []

class IntentClassificationAction(Action):
    def name(self) -> str:
        return "action_intent_classification"

    def __init__(self):
        # Load the model and tokenizer
        self.model = BertForSequenceClassification.from_pretrained("C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\models\\intent_classification_model")
        self.tokenizer = BertTokenizer.from_pretrained("C:\\Users\\DELL\\Desktop\\programming\\VsCodeProjects\\WID3002_NLP\\models\\intent_classification_tokenizer")

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Get the user message
        user_message = tracker.latest_message.get('text')

        # Tokenize and encode the text
        inputs = self.tokenizer(user_message, return_tensors='pt', padding=True, truncation=True)

        # Perform inference
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_idx = torch.argmax(logits, dim=1).item()

        # Get the predicted intent label
        predicted_intent = model.config.id2label[predicted_class_idx]

        # Utter the predicted intent
        dispatcher.utter_message(text=f"Predicted Intent: {predicted_intent}")

        return []
class ActionILAMA3(Action):
    def name(self) -> str:
        return "action_ilama3"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get('text')
        ilama3_response = generate_ilama3_response(user_message)
        dispatcher.utter_message(text=ilama3_response)
        return []
