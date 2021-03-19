class MenuHelper:
    def __init__(self, app):
        self.app = app

    def home(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/") and len(wd.find_elements_by_name("searchstring")) > 0):
            wd.find_element_by_link_text("home").click()

    def groups(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("groups.php") and len(wd.find_elements_by_name("new")) > 0):
            wd.find_element_by_link_text("groups").click()
