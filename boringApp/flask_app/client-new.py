import requests


class Activity(object):
    def __init__(self, json_data):
        self.activity = json_data["Activity"]
        self.availability = json_data["Availability"]
        self.type= json_data["Type"]
        self.participants = json_data["Participants"]
        self.price = json_data["Price"]
        self.accessibility = json_data["Accessibility"]
        self.duration = json_data["Duration"]
        self.kid_friendly = json_data["Kid_Friendly"]
        self.link = json_data["Link"]
        self.key = json_data["Key"]

    def __repr__(self):
        return self.activity


class ActivityClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = "https://bored-api.appbrewery.com/"

    def get_random_activity(self):
        url = f"{self.base_url}/random"
        resp = self.sess.get(url)

        if resp.status_code != 200:
            raise ValueError("Failed to request random activity")

        data = resp.json()

        return Activity(data)

    def get_filtered_activities(self, activity_type=None, participants=None):
        params = {}
        if activity_type:
            params["type"] = activity_type
        if participants:
            params["participants"] = participants
        
        url = f"{self.base_url}/filter"
        resp = self.sess.get(url, params=params)

        if resp.status_code != 200:
            raise ValueError("Failed to request filtered activities")

        data = resp.json()

        if not isinstance(data, list):
            raise ValueError("Error in filter")

        return [Activity(item) for item in data]
