import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pybreaker
import logging
from core.middlewares import get_current_correlation_id

logger = logging.getLogger(__name__)

user_service_cb = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=30)


def get_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session


@user_service_cb
def fetch_author_data(author_id: int, cookies: dict = None) -> dict:
    session = get_session()
    url = f"http://users-service:8001/api/users/v1/users/users/{author_id}/"
    headers = {'X-Correlation-ID': get_current_correlation_id()}

    response = session.get(url, timeout=(2.0, 5.0), cookies=cookies, headers=headers)
    response.raise_for_status()
    return response.json()
