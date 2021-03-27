import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.application import Application
from fixture.db import DbFixture


fixture = None
config = None


def load_config(file):
    global config
    if config is None:
        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(conf_file_path) as config_file:
            config = json.load(config_file)
    return config


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--config"))["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])

    fixture.session.ensure_login(name=web_config["login"], pwd=web_config["password"])

    return fixture


@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--config"))["db"]

    dbfixture = DbFixture(host=db_config["host"],
                          name=db_config["name"],
                          user=db_config["user"],
                          password=db_config["password"])

    def finalizer():
        dbfixture.destroy()
    request.addfinalizer(finalizer)
    return dbfixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global fixture

    def finalizer():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(finalizer)
    return fixture


@pytest.fixture()
def check_ui(request):
    return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--config", action="store", default="config.json")
    parser.addoption("--check_ui", action="store")

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[repr(g) for g in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[repr(g) for g in testdata])


def load_from_module(module):
    return importlib.import_module(f'data.{module}').testdata


def load_from_json(jsonfile):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'data/{jsonfile}.json')) as file:
        return jsonpickle.decode(file.read())
