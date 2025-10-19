import json

class Response:
    """Class to hold response data."""
    def __init__(self, status_code: int, message: str, data: dict = None):
        self.status_code = status_code
        self.message = message
        self.data = data or {}

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data
        }

    def to_json(self):
        return json.dumps(self.to_dict())