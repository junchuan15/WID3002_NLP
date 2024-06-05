# actions.py
from typing import Any, Text, Dict, List, Tuple, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
import requests
from rasa_sdk.events import SlotSet
from datetime import datetime


class ActionGetLocationInfo(Action):
    def name(self) -> Text:
        return "action_get_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api_key = "AIzaSyCaWAF9DCj2P6d6asrh-b61BNua3zD2gMQ"
        location_entity = next(tracker.get_latest_entity_values("location"), None)
        
        if location_entity:
            address, latitude, longitude = self.get_location_coordinates(location_entity, api_key)
        
            if address is not None:
                sentence = f"It is at {address}."
                radius = 100
                places = self.get_nearby_places(latitude, longitude, api_key, radius)
                if places:
                    nearby_places = [place['name'] for place in places]
                    if len(nearby_places) == 1:
                        sentence += f" It is near to {nearby_places[0]}."
                    elif len(nearby_places) > 1:
                        sentence += f" It is near to {', '.join(nearby_places[:-1])}, and {nearby_places[-1]}."
                dispatcher.utter_message(text=sentence)
            else:
                dispatcher.utter_message(text="Failed to retrieve the location information.")
        else:
            dispatcher.utter_message(text="No location entity found in the user message.")
        
        return []

    def get_location_coordinates(self, location_name: Text, api_key: Text) -> Tuple[Text, float, float]:
        endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location_name,
            "key": api_key
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if data['status'] == 'OK':
            results = data['results'][0]
            formatted_address = results['formatted_address']
            location = results['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return formatted_address, latitude, longitude
        else:
            print("Error:", data['status'])
            return None, None, None

    def get_nearby_places(self, latitude: float, longitude: float, api_key: Text, radius: int) -> List[Dict[Text, Any]]:
        endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "key": api_key
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if data['status'] == 'OK':
            return data['results']
        else:
            print("Error:", data['status'])
            return []

class ActionProvideActivities(Action):
    def name(self) -> Text:
        return "action_provide_activities"

    def normal_date(self, date_str: Text) -> Optional[Text]:
        date_formats = ["%d/%m/%Y", "%d %B %Y", "%d %B", "%d %b", "%d %b %Y"]
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date = tracker.get_slot('date')

        activities = {
            "2023-09-30": (
            "The activities for 30 September 2023 (Saturday) include: "
            "\n9:00 AM - 10:00 AM: Registration,\n"
            "10:00 AM - 11:00 AM: Distribution of MHS Kit,\n"
            "11:00 AM - 12:30 PM: Session with Residential College (RC) Management [Location: Residential Colleges],\n"
            "12:30 PM - 2:30 PM: Program Pengenalan Asas Kesedaran Mengundi Kepada Pelajar Baharu Institusi Pendidikan Tinggi (IPT) [Location: Dewan Tunku Canselor],\n"
            "2:30 PM - 3:30 PM: Student Carnival Activities [Location: Residential College],\n"
            "3:30 PM - 4:00 PM: Break Time,\n"
            "4:00 PM - 5:00 PM: Closing Ceremony UM-WOW:MHS 2023/2024 [Location: UM Arena],\n"
            "5:30 PM - 7:00 PM: Session with Pemudahcara Mahasiswa (PM) [Location: Residential Colleges],\n"
            "7:00 PM - 8:00 PM: Residential Colleges' Activities,\n"
            "8:30 PM - 9:30 PM: Residential Colleges' Activities,\n"
            "9:30 PM - 10:30 PM: Residential Colleges' Activities,\n"
            "10:30 PM - 11:30 PM: Residential Colleges' Activities"
            ),
            "2023-10-01": (
            "The activities for 1 October 2023 (Sunday) include: "
            "\n9:00 AM - 10:00 AM: Opening Ceremony and New Students Pledge by Dato' Vice-Chancellor [Location: Dewan Tunku Canselor],\n"
            "10:00 AM - 11:00 AM: Break Time,\n"
            "11:00 AM - 12:30 PM: Session with UM Clinic, Bursar, Library, Security Department, OSHREC, Counselling and Disability Empowerment Division [Location: Dewan Tunku Canselor],\n"
            "12:30 PM - 2:30 PM: Activities in the Faculty [Location: Faculties],\n"
            "2:30 PM - 3:30 PM: Program Industri: Ericsson & Talent Corp [Location: Dewan Tunku Canselor],\n"
            "3:30 PM - 4:00 PM: Break Time,\n"
            "4:00 PM - 5:00 PM: Program Madani (KPT) [Location: Dewan Tunku Canselor],\n"
            "5:30 PM - 7:00 PM: Introduction to SUKSIS & PALAPES [Location: Dewan Tunku Canselor],\n"
            "7:00 PM - 8:00 PM: Break Time,\n"
            "8:30 PM - 9:30 PM: Session Registration 1,\n"
            "9:30 PM - 10:30 PM: Session Registration 2,\n"
            "10:30 PM - 11:30 PM: Session Registration 3"
            ),
            "2023-10-02": (
            "The activities for 2 October 2023 (Monday) include: "
            "\n9:00 AM - 10:00 AM: Session with Deputy Vice-Chancellor (Academic & International) [Location: Dewan Tunku Canselor],\n"
            "10:00 AM - 11:00 AM: Break Time,\n"
            "11:00 AM - 12:30 PM: Program Industri: Ericsson & Talent Corp [Location: Dewan Tunku Canselor],\n"
            "12:30 PM - 2:30 PM: Session Registration 4,\n"
            "2:30 PM - 3:30 PM: Activities in the Faculty [Location: Faculties],\n"
            "3:30 PM - 4:00 PM: Break Time,\n"
            "4:00 PM - 5:00 PM: Session with Deputy Vice-Chancellor (Student Affairs) & Student Affairs Department [Location: Dewan Tunku Canselor],\n"
            "5:30 PM - 7:00 PM: Program Madani (KPT) [Location: Dewan Tunku Canselor],\n"
            "7:00 PM - 8:00 PM: Break Time,\n"
            "8:30 PM - 9:30 PM: Student Carnival Activities [Location: Dewan Tunku Canselor],\n"
            "9:30 PM - 10:30 PM: Break Time,\n"
            "10:30 PM - 11:30 PM: Activities in the Faculty [Location: Faculties]"
            ),
            "2023-10-03": (
            "The activities for 3 October 2023 (Tuesday) include: "
            "\n9:00 AM - 10:00 AM: Session Registration 1,\n"
            "10:00 AM - 11:00 AM: Break Time,\n"
            "11:00 AM - 12:30 PM: Student Carnival Activities [Location: Dewan Tunku Canselor],\n"
            "12:30 PM - 2:30 PM: Activities in the Faculty [Location: Faculties],\n"
            "2:30 PM - 3:30 PM: Break Time,\n"
            "3:30 PM - 4:00 PM: Break Time,\n"
            "4:00 PM - 5:00 PM: Session with UM Clinic, Bursar, Library, Security Department, OSHREC, Counselling and Disability Empowerment Division [Location: Dewan Tunku Canselor],\n"
            "5:30 PM - 7:00 PM: Activities in the Faculty [Location: Faculties],\n"
            "7:00 PM - 8:00 PM: Break Time,\n"
            "8:30 PM - 9:30 PM: Session Registration 2,\n"
            "9:30 PM - 10:30 PM: Session Registration 4,\n"
            "10:30 PM - 11:30 PM: Activities in the Faculty [Location: Faculties]"
            ),
            "2023-10-04": (
            "The activities for 4 October 2023 (Wednesday) include: "
            "\n9:00 AM - 10:00 AM: Session Registration 1,\n"
            "10:00 AM - 11:00 AM: Break Time,\n"
            "11:00 AM - 12:30 PM: Student Carnival Activities [Location: Dewan Tunku Canselor],\n"
            "12:30 PM - 2:30 PM: Activities in the Faculty [Location: Faculties],\n"
            "2:30 PM - 3:30 PM: Break Time,\n"
            "3:30 PM - 4:00 PM: Break Time,\n"
            "4:00 PM - 5:00 PM: Session with UM Clinic, Bursar, Library, Security Department, OSHREC, Counselling and Disability Empowerment Division [Location: Dewan Tunku Canselor],\n"
            "5:30 PM - 7:00 PM: Activities in the Faculty [Location: Faculties],\n"
            "7:00 PM - 8:00 PM: Break Time,\n"
            "8:30 PM - 9:30 PM: Session Registration 2,\n"
            "9:30 PM - 10:30 PM: Session Registration 4,\n"
            "10:30 PM - 11:30 PM: Activities in the Faculty [Location: Faculties]"
            ),
            "2023-10-05": (
            "The activities for 5 October 2023 (Thursday) include: "
            "\n9:00 AM - 10:00 AM: Session Registration 1,\n"
            "10:00 AM - 11:00 AM: Break Time,\n"
            "11:00 AM - 12:30 PM: Student Carnival Activities [Location: Dewan Tunku Canselor],\n"
            "12:30 PM - 2:30 PM: Activities in the Faculty [Location: Faculties],\n"
            "2:30 PM - 3:30 PM: Break Time,\n"
            "3:30 PM - 4:00 PM: Break Time,\n"
            "4:00 PM - 5:00 PM: Session with UM Clinic, Bursar, Library, Security Department, OSHREC, Counselling and Disability Empowerment Division [Location: Dewan Tunku Canselor],\n"
            "5:30 PM - 7:00 PM: Activities in the Faculty [Location: Faculties],\n"
            "7:00 PM - 8:00 PM: Break Time,\n"
            "8:30 PM - 9:30 PM: Session Registration 2,\n"
            "9:30 PM - 10:30 PM: Session Registration 4,\n"
            "10:30 PM - 11:30 PM: Activities in the Faculty [Location: Faculties]"
                )
            }
        
        if date:
            normalized_date = self.normal_date(date)
            details = activities.get(normalized_date)
            if details:
                dispatcher.utter_message(text=details)
            else:
                dispatcher.utter_message(text="UM-WOW ended on 5 October 2023")
            return [SlotSet("date_requested", False)]
        else:
            return [SlotSet("date_requested", True)]
        
class ActionAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date_requested = tracker.get_slot('date_requested')
        if date_requested:
            dispatcher.utter_message(text="Could you please specify the date?")
        return []
    
class ActionProvideRegistrationProcess(Action):
    def name(self) -> Text:
        return "action_provide_registration_process"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reg_place = tracker.get_slot('reg_place')
        reg_place_requested = tracker.get_slot('reg_place_requested')

        registration_details = {
            "padang kawad palapes": (
                "The registration process at Padang Kawad Palapes is as follows:\n"
                "1. Parents/Guardians enter the POA area and follow staff guidance to park their vehicle.\n"
                "2. Students register at the registration tent. Parents/Guardians place the student's personal items in the designated luggage area at the registration tent.\n"
                "3. After registration, students should load personal items onto the shuttle bus with the help of staff.\n"
                "4. Only students will proceed to the assigned residential college using the provided shuttle bus.\n"
                "5. Parents/Guardians must leave the campus once the student has boarded the shuttle bus. They are not allowed to be at the residential college area throughout the registration day."
            ),
            "kk9": (
                "The registration process at Kolej Kediaman Tun Syed Zahiruddin (KK9) is as follows:\n"
                "1. Only one vehicle per family is allowed into the POA. Registration is conducted via a drive-in system, with staff guiding the vehicle parking.\n"
                "2. Students and parents/guardians have 10 minutes to place the student’s personal items in the designated luggage tent.\n"
                "3. Students proceed to the registration area in the Administration Block. Parents/Guardians must leave the POA after unloading the student’s belongings to make way for other vehicles. They are not allowed in the residential college area throughout the registration day."
            )
        }

        if reg_place:
            normalized_reg_place = reg_place.strip().lower()
            details = registration_details.get(normalized_reg_place)
            if details:
                dispatcher.utter_message(text=details)
                return [SlotSet("reg_place_requested", False)]
            else:
                dispatcher.utter_message(text="I'm sorry, I don't have the registration details for that place.")
            return [SlotSet("reg_place_requested", False)]
        else:
            return [SlotSet("reg_place_requested", True)]

class ActionAskRegPlace(Action):
    def name(self) -> Text:
        return "action_ask_reg_place"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reg_place_requested = tracker.get_slot('reg_place_requested')
        if reg_place_requested:
            dispatcher.utter_message(text="Where is your assigned registration location?")
        return []
    
class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [Restarted()]
    
class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        dispatcher.utter_message(
            text="I'm sorry, I do not have that information. Please refer to the UM official websites 'https://um.edu.my/' to check for latest updates."
        )
        return [UserUtteranceReverted()]