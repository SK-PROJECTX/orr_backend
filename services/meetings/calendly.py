import requests
import logging
from django.conf import settings
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class CalendlyAPIException(APIException):
    status_code = 400
    default_detail = "An error occurred while communicating with Calendly."
    default_code = "calendly_error"


class CalendlyAPI:
    BASE_URL = "https://api.calendly.com"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.CALENDLY_API_KEY}",
            "Content-Type": "application/json",
        }
        self.user_uri = None 
    def _request(self, method, url, **kwargs):
        """
        Unified request wrapper with full logging.
        """
        logger.error("CALENDLY REQUEST")
        logger.error(f"➡ Method: {method}")
        logger.error(f"➡ URL: {url}")
        logger.error(f"➡ Headers: {self.headers}")

        if "params" in kwargs:
            logger.error(f"➡ Query Params: {kwargs['params']}")

        if "json" in kwargs:
            logger.error(f"➡ JSON Payload: {kwargs['json']}")

        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)

            logger.error(" CALENDLY RESPONSE")
            logger.error(f"⬅ Status Code: {response.status_code}")
            logger.error(f"⬅ Raw Response: {response.text}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error(" HTTP ERROR from Calendly")
            logger.error(f"Status: {response.status_code}")
            logger.error(f"Response text: {response.text}")

            try:
                error_data = response.json()
                message = (
                    error_data.get("title")
                    or error_data.get("message")
                    or str(e)
                )
            except Exception:
                message = str(e)

            raise CalendlyAPIException(
                detail=f"Calendly API error: {message}"
            )

        except requests.exceptions.RequestException as e:
            logger.error(" Network error talking to Calendly")
            logger.error(str(e))

            raise CalendlyAPIException(
                detail=f"Network error communicating with Calendly: {str(e)}"
            )
    def get_user_uri(self):
        """Fetch and cache the user URI"""
        if not self.user_uri:
            url = f"{self.BASE_URL}/users/me"
            data = self._request("GET", url)
            self.user_uri = data["resource"]["uri"]
        return self.user_uri
    def get_event_types(self):
        """Fetch all event types for the authenticated user"""
        url = f"{self.BASE_URL}/event_types"
        params = {"user": self.get_user_uri()}
        return self._request("GET", url, params=params)

    def get_available_slots(self, event_type_uri, start_date, end_date):
        url = f"{self.BASE_URL}/event_type_available_times"
        params = {
            "event_type": event_type_uri,
            "start_time": start_date.isoformat(),
            "end_time": end_date.isoformat(),
        }
        return self._request("GET", url, params=params)

    def create_event(self, event_type_uri, invitee_email, start_time, name):
        url = f"{self.BASE_URL}/scheduled_events"
        payload = {
            "event_type": event_type_uri,
            "start_time": start_time,
            "invitees": [
                {"email": invitee_email, "name": name}
            ],
        }
        return self._request("POST", url, json=payload)

    def cancel_event(self, event_uuid, reason="Cancelled"):
        url = f"{self.BASE_URL}/scheduled_events/{event_uuid}/cancellation"
        payload = {"reason": reason}
        return self._request("POST", url, json=payload)
