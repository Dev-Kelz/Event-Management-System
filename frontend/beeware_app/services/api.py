class ApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url

    def get_events(self):
        return {"events": []}
