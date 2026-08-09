import os

from services.apis.base_api import BaseAPI


class JobsAPI(BaseAPI):

    BASE_URL = "https://jsearch.p.rapidapi.com/search"

    def search_jobs(

        self,

        keyword,

        location="India",

        page=1

    ):

        headers = {

            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),

            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"

        }

        params = {

            "query": f"{keyword} in {location}",

            "page": page,

            "num_pages": 1

        }

        return self.get(

            self.BASE_URL,

            headers=headers,

            params=params

        )