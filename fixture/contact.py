from selenium.webdriver.support.ui import Select
from model.contact import Contact
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from random import randint


class ContactHelper:
    def __init__(self, app):
        self.app = app
        self.menu = app.menu

    def create(self, contact: Contact):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()

        self.fill_contact(contact)

        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()

        self.menu.home()

        self.contact_cache = None

    def edit_any_contact(self, contact: Contact) -> (int, Contact):
        wd = self.app.wd
        self.menu.home()

        entry_list = wd.find_elements_by_xpath("//tr[@name='entry']")
        assert len(entry_list) > 0

        index = randint(0, len(entry_list) - 1)
        entry = entry_list[index]

        edit = entry.find_element_by_xpath(".//img[@title='Edit']")
        edit.click()

        contact_old_state = self.grab_data()
        self.fill_contact(contact)

        update = wd.find_element_by_xpath("//input[@type='submit'][@value='Update']")
        update.click()

        self.menu.home()

        self.contact_cache = None

        return index, contact_old_state

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.menu.home()
            self.contact_cache = []

            for elem in wd.find_elements_by_xpath("//tr[@name='entry']"):
                contact_id = elem.find_element_by_name("selected[]").get_attribute("value")
                lastname = elem.find_element_by_xpath("./td[2]").text
                firstname = elem.find_element_by_xpath("./td[3]").text
                address = elem.find_element_by_xpath("./td[4]").text
                emails = elem.find_element_by_xpath("./td[5]").text
                phones = elem.find_element_by_xpath("./td[6]").text
                self.contact_cache.append(Contact(id=contact_id,
                                                  lastname=lastname,
                                                  firstname=firstname,
                                                  address=address,
                                                  emails=emails,
                                                  phones=phones))

        return self.contact_cache

    def get_contact_from_edit_page(self, index: int):
        wd = self.app.wd
        self.menu.home()
        entry_list = wd.find_elements_by_xpath("//tr[@name='entry']")
        assert len(entry_list) > 0

        entry = entry_list[index]

        edit = entry.find_element_by_xpath(".//img[@title='Edit']")
        edit.click()

        return self.grab_data()

    def grab_data(self) -> Contact:
        wd = self.app.wd

        id = wd.find_element_by_name("id").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        address = wd.find_element_by_name("address").get_attribute("value")
        phone_home = wd.find_element_by_name("home").get_attribute("value")
        phone_work = wd.find_element_by_name("work").get_attribute("value")
        mobile = wd.find_element_by_name("mobile").get_attribute("value")
        phone_secondary = wd.find_element_by_name("phone2").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email_secondary = wd.find_element_by_name("email2").get_attribute("value")
        email_other = wd.find_element_by_name("email3").get_attribute("value")

        return Contact(id=id, lastname=lastname, firstname=firstname, address=address,
                       phone_home=phone_home, phone_work=phone_work, mobile=mobile, phone_secondary=phone_secondary,
                       email_main=email, email_secondary=email_secondary, email_other=email_other)

    def fill_contact(self, contact):
        self.type_in_field("firstname", contact.firstname)
        self.type_in_field("middlename", contact.middlename)
        self.type_in_field("lastname", contact.lastname)
        self.type_in_field("nickname", contact.nickname)

        self.type_in_field("title", contact.title)
        self.type_in_field("company", contact.company)
        self.type_in_field("address", contact.address)

        self.type_in_field("home", contact.phone_home)
        self.type_in_field("mobile", contact.mobile)
        self.type_in_field("work", contact.phone_work)
        self.type_in_field("fax", contact.fax)

        self.type_in_field("email", contact.email_main)
        self.type_in_field("email2", contact.email_secondary)
        self.type_in_field("email3", contact.email_other)
        self.type_in_field("homepage", contact.homepage)

        self.select_in_field("bday", contact.bday)
        self.select_in_field("bmonth", contact.bmonth)
        self.type_in_field("byear", contact.byear)

        self.select_in_field("aday", contact.aday)
        self.select_in_field("amonth", contact.amonth)
        self.type_in_field("ayear", contact.ayear)

        self.type_in_field("address2", contact.address_secondary)
        self.type_in_field("phone2", contact.phone_secondary)
        self.type_in_field("notes", contact.notes)

    def type_in_field(self, field_name, value):
        wd = self.app.wd
        if value is not None:
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(value)

    def select_in_field(self, selector_name, value):
        wd = self.app.wd
        if value is not None:
            selector = Select(wd.find_element_by_name(selector_name))
            selector.select_by_visible_text(value)

    def delete_any_contact_from_itself(self):
        wd = self.app.wd
        self.menu.home()

        entry_list = wd.find_elements_by_xpath("//tr[@name='entry']")
        assert len(entry_list) > 0

        entry = entry_list[randint(0, len(entry_list) - 1)]

        contact_id = entry.find_element_by_name("selected[]").get_attribute("value")
        edit = entry.find_element_by_xpath(".//img[@title='Edit']")
        edit.click()

        delete = wd.find_element_by_xpath("//input[@type='submit'][@value='Delete']")
        delete.click()

        self.menu.home()
        self.contact_cache = None

        return contact_id

    def delete_any_contact_form_list(self):
        wd = self.app.wd
        self.menu.home()

        entry_list = wd.find_elements_by_xpath("//tr[@name='entry']")
        assert len(entry_list) > 0

        entry = entry_list[randint(0, len(entry_list) - 1)]
        contact_id = entry.find_element_by_name("selected[]").get_attribute("value")

        checkbox = entry.find_element_by_name("selected[]")
        checkbox.click()

        delete = wd.find_element_by_xpath("//input[@type='button'][@value='Delete']")
        delete.click()

        try:
            WebDriverWait(wd, 1).until(EC.alert_is_present(), 'Не дождались алёрта')
            alert = wd.switch_to.alert
            alert.accept()
            wd.find_element_by_css_selector("div.msgbox")
        except TimeoutException:
            print("no alert")
        finally:
            self.menu.home()
            self.contact_cache = None

            return contact_id

    def count(self):
        wd = self.app.wd
        self.menu.home()

        return len(wd.find_elements_by_name("selected[]"))
