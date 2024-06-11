from api import CanvasAPI

class CanvasClient:
    def __init__(self):
        self.canvas_api = None
        self.token = None
        self.selected_course = None

    def start(self):
        while True:
            if not self.token:
                self._prompt_for_token()
            elif not self.canvas_api:
                self.canvas_api = CanvasAPI(self.token)
            elif not self.selected_course:
                self._prompt_for_course()
            else:
                self._list_assignments()

    def _prompt_for_token(self):
        self.token = input("Enter your token: ")

    def _prompt_for_course(self):
        courses = self.canvas_api.get_current_courses()
        for i, course in enumerate(courses, start=1):
            print(f"{i}. {course['name']}")
        course_number = int(input("Select a course by number, or 0 to sign out: "))
        if course_number == 0:
            self.token = None
            self.canvas_api = None
        else:
            self.selected_course = courses[course_number - 1]

    def _list_assignments(self):
        assignments = self.canvas_api.get_course_assignments(self.selected_course['id'])
        for assignment in assignments:
            print(assignment['name'])
        action = input("Enter 'b' to go back, '0' to sign out, or an assignment name to view it: ")
        if action == 'b':
            self.selected_course = None
        elif action == '0':
            self.token = None
            self.canvas_api = None
            self.selected_course = None
        else:
            # TODO: Implement viewing an assignment
            print(f"Viewing assignment '{action}'")
