from behave import when, then
from hamcrest import assert_that
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sogeti.browser.menu import find_menu_element_with_text, find_menu_link_element_with_text
from sogeti.browser.settings import max_wait_seconds


@when('we load the web page "{url}"')
def step_impl(context, url):
    context.browser.get(url)


@then('the web page\'s title is "{title}"')
def step_impl(context, title):
    assert_that(title.strip() == context.browser.title.strip())


@then('the web page\'s heading is "{heading}"')
def step_impl(context, heading):
    h1_elem = WebDriverWait(context.browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1")))
    span_elem = h1_elem.find_element_by_tag_name("span")
    assert_that(span_elem.text == heading)


@when('we hover menu "{menu_text}"')
def step_impl(context, menu_text):
    menu_elem = find_menu_element_with_text(context.browser, menu_text)
    move_action = ActionChains(context.browser).move_to_element(menu_elem)
    move_action.perform()


@when('we click menu "{menu_text}"')
def step_impl(context, menu_text):
    menu_elem = find_menu_element_with_text(context.browser, menu_text)
    menu_elem.click()


@when('we click menu link "{menu_text}::{link_text}"')
def step_impl(context, menu_text, link_text):
    menu_link_elem = find_menu_link_element_with_text(context.browser, menu_text, link_text)
    menu_link_elem.click()


@then('menu "{menu_text}" is displayed as selected')
def step_impl(context, menu_text):
    menu_elem = find_menu_element_with_text(context.browser, menu_text)
    li_elem = menu_elem.find_element_by_xpath("../..")

    # When a menu is selected, its CSS class differs from others'.
    class_names = li_elem.get_attribute("class")
    assert_that("selected" in class_names)
    assert_that("expanded" in class_names)


@then('menu link "{menu_text}::{link_text}" is displayed as selected')
def step_impl(context, menu_text, link_text):
    menu_link_elem = find_menu_link_element_with_text(context.browser, menu_text, link_text)
    li_elem = menu_link_elem.find_element_by_xpath("..")

    # When a menu link is selected, its CSS class differs from others'.
    class_names = li_elem.get_attribute("class")
    assert_that("selected" in class_names)
    assert_that("current" in class_names)


@when('we scroll down to form "{form_heading}"')
def step_impl(context, form_heading):
    xpath = "//form/h2[text()='{}']".format(form_heading)
    heading_elem = WebDriverWait(context.browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    context.contact_form = heading_elem.find_element_by_xpath("..")

    # Scroll down to the form.
    context.browser.execute_script("window.scrollTo(0, {})".format(heading_elem.location["y"]))
    move_action = ActionChains(context.browser).move_to_element(heading_elem)
    move_action.perform()


def build_text_field_dict(context):
    result_dict = dict()
    # The form has six labels. But the last one is to contain the checkbox. It has no "for" attribute.
    label_elem_list = context.contact_form.find_elements_by_xpath(".//label[@for]")
    for label_elem in label_elem_list:
        text_field_id = label_elem.get_attribute("for")
        result_dict[label_elem.text] = context.browser.find_element_by_id(text_field_id)
    return result_dict


@when('we fill the contact form\'s text fields as below')
def step_impl(context):
    text_field_dict = build_text_field_dict(context)
    for row in context.table:
        text_field_dict[row["field"]].send_keys(row["text"])


@when('we click the contact form\'s check box "{checkbox_text}"')
def step_impl(context, checkbox_text):
    xpath = ".//input[@type='checkbox' and @value='{}']".format(checkbox_text)
    checkbox_elem = WebDriverWait(context.contact_form, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    checkbox_elem.click()


@when('we click the contact form\'s submit button')
def step_impl(context):
    xpath = ".//button[@type='submit']"
    button_elem = WebDriverWait(context.contact_form, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    button_elem.click()


@then('the contact form displays success with message "{message_text}"')
def step_impl(context, message_text):
    xpath = ".//div[@class='Form__Status']/div"
    div_elem = WebDriverWait(context.contact_form, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

    # Make sure that we get the "success" message.
    class_names = div_elem.get_attribute("class")
    assert_that("Form__Status__Message" in class_names)
    assert_that("Form__Success__Message" in class_names)

    paragraph_elem = div_elem.find_element_by_tag_name("p")
    assert_that(message_text.strip() == paragraph_elem.text.strip())


@then('the country drop-down list is visible')
def step_impl(context):
    xpath = "//div[@class='country-list']"
    div_elem = WebDriverWait(context.browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    style = div_elem.get_attribute("style")
    assert_that(len(style.strip()) > 0)


@then('the country drop-down list is invisible')
def step_impl(context):
    xpath = "//div[@class='country-list']"
    div_elem = WebDriverWait(context.browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    style = div_elem.get_attribute("style")
    assert_that(len(style.strip()) <= 0)


@when('we click the drop-down button "{button_text}"')
def step_impl(context, button_text):
    xpath = "//div[@class='navbar-global']/span"
    span_elem = WebDriverWait(context.browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    span_elem.click()


@then('the country links are linked correctly')
def step_impl(context):
    # Get the links.
    xpath = "//div[@class='country-list']"
    div_elem = WebDriverWait(context.browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    link_elem_list = div_elem.find_elements_by_xpath("./ul/li/a")

    # Build a map for the links, in order to access the url easily with the data in the test table.
    link_elem_dict = dict()
    for link_elem in link_elem_list:
        link_elem_dict[link_elem.text.upper()] = link_elem.get_attribute("href")

    # Verify each row in the test table.
    for row in context.table:
        assert_that(row["country"].upper() in link_elem_dict)
        context.execute_steps("""
            When we load the web page "{}"
            Then the web page's title is "{}" 
        """.format(link_elem_dict[row["country"].upper()], row["result page title"]))
