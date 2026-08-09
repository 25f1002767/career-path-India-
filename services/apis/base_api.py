import requests


class BaseAPI:

    def get(self, url, headers=None, params=None):

        try:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=20
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            print("API ERROR:", e)

            return None