import requests


class Activity(object):
    def __init__(self, json_data):
        self.activity = json_data["activity", "no activity found"]
        self.availability = json_data["availability", 0.0]
        self.type= json_data["type", "n/a"]
        self.participants = json_data["participants", 0]
        self.price = json_data["price", 0.0]
        self.accessibility = json_data["accessibility", "n/a"]
        self.duration = json_data["duration", "n/a"]
        self.kid_friendly = json_data["kidFriendly", False]
        self.link = json_data["link", "n/a"]
        self.key = json_data["key", "n/a"]

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

    def get_filtered_activity(self, activity_type=None, participants=None):
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

        if not isinstance(data, list) or not data:
            raise ValueError("Error in filter")

        return Activity(data[0])
