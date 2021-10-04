import requests
from urllib3.util.retry import Retry


class GoogleApiClient:

    def __init__(self, config):
        self._api = config['api']
        self._http = config.get('http', {})

        adapter = requests.adapters.HTTPAdapter(
            max_retries=Retry(
                total=self._http.get('retries', 3),
                backoff_factor=self._http.get('delay', 0.1),
            )
        )

        self._session = requests.Session()
        self._session.mount('https://', adapter)

    def fetch_geo_data(self, latlng):
        resp = self._session.get(
            url=self._api['url'],
            params={
                'latlng': latlng,
                'key': self._api['key'],
                'result_type': self._api.get('result_type', '')
            },
            timeout=self._http.get('timeout', 0.1),
        ).json()

        if resp['status'] != 'OK':
            raise RuntimeError('Invalid response: {}'.format(resp['status']))
        return resp
