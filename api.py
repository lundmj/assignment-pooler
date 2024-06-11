import json
import requests

from url_config import *

class CanvasAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def _save_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def _get_request(self, endpoint):
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

    def _get_paginated_data(self, url):
        """When the API response has multiple pages, 
        this function will get all the data from 
        all pages."""
        data = []
        while url:
            response = requests.get(url, headers=self.headers)
            data.extend(response.json())
            links = response.links
            url = links['next']['url'] if 'next' in links else None
        return data

    def _get_user(self):
        return self._get_request(SELF_ID)

    def _get_user_id(self):
        result = self._get_user()
        return result.get('id', None)

    def get_current_courses(self):
        return self._get_paginated_data(CURRENT_COURSES)

    def get_course_assignments(self, course_id):
        url = COURSE_ASSIGNMENTS.format(self._get_user_id(), course_id)
        return self._get_paginated_data(url)

    def get_assignment_submission(self, course_id, assignment_id):
        url = ASSIGNMENT_SUBMISSION.format(course_id, assignment_id, self._get_user_id())
        return self._get_request(url)

