import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.application import Application


fixture = None
config = None


@pytest.fixture
def app(request):
    global fixture
    global config
    browser = request.config.getoption("--browser")
    if config is None:
        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption("--config"))
        with open(conf_file_path) as config_file:
            config = json.load(config_file)
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config["baseUrl"])

    fixture.session.ensure_login(name=config["login"], pwd=config["password"])

    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global fixture

    def finalizer():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(finalizer)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--config", action="store", default="config.json")


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
