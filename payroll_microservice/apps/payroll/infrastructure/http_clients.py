import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pybreaker
from rest_framework.exceptions import ValidationError

user_service_cb = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=30)


def get_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session


@user_service_cb
def check_user_exists(user_id: int, cookies: dict = None):
    session = get_session()
    url = f"http://users-service:8001/v1/users/users/{user_id}/"

    try:
        response = session.get(url, timeout=(2.0, 5.0), cookies=cookies)

        if response.status_code == 404:
            raise ValidationError({"user": ["User with such id does not exist."]})

        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValidationError({"detail": f"User service is unavailable right now. {e}"})
