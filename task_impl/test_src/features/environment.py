import configparser

from behave import fixture
from behave.fixture import use_fixture_by_tag
from selenium import webdriver


@fixture
def browser_firefox(context, timeout=30, **kwargs):
    context.browser = webdriver.Firefox()
    yield context.browser
    context.browser.close()


@fixture
def browser_chrome(context, timeout=30, **kwargs):
    read_options_to_context(r"..\options.ini", context)
    context.browser = webdriver.Chrome(context.chrome_path)
    yield context.browser
    context.browser.quit()


fixture_registry = {
    "fixture.browser.firefox": browser_firefox,
    "fixture.browser.chrome": browser_chrome,
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)


def read_options_to_context(file_path, context):
    config = configparser.ConfigParser()
    config.read(file_path)
    context.chrome_path = config["DEFAULT"]["chromedriver"]
