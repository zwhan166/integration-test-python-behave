from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sogeti.browser.settings import max_wait_seconds


def find_menu_element_with_text(browser, menu_text):
    xpath = "//nav[@class='main-menu-desktop']/ul/li/div/span[text()='{}']".format(menu_text)
    menu_elem = WebDriverWait(browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    return menu_elem


def find_menu_link_element_with_text(browser, menu_text, link_text):
    span_xpath = "//header/div/div/span[text()='{}']".format(menu_text)
    span_elem = WebDriverWait(browser, max_wait_seconds).until(
        EC.presence_of_element_located((By.XPATH, span_xpath)))
    link_elem = span_elem.find_element_by_xpath("./../ul/li/a[text()='{}']".format(link_text))
    return link_elem
