from selenium import webdriver
from fixture.session import SessionHelper
from fixture.menu import MenuHelper
from fixture.group import GroupHelper
from fixture.contact import ContactHelper


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()  # 'C:\\Tools\\chromedriver.exe')
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError(f'Unrecognized browser {browser}\nBrowser should be [firefox|chrome|edge]')
        self.wd.implicitly_wait(0.1)
        self.session = SessionHelper(self)
        self.menu = MenuHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_index_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
