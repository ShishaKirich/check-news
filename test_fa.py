from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pytest

@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install())
    )
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def wait(browser):
    return WebDriverWait(browser, 10)


def test_element(browser, wait):
    browser.get("https://www.fa.ru/university/structure/scientific-educational-departments/itabd/ib/")
    text = 'Кафедра информационной безопасности обеспечивает подготовку высококвалифицированных специалистов в области защиты информации. '
    wait.until(EC.presence_of_element_located((By.XPATH, f'//p[text()="{text}"]')))



def test_open(browser, wait):
    browser.get("https://www.fa.ru/university/structure/scientific-educational-departments/itabd/ib/")
    # Ожидание загрузки результатов
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//h1"))
    )
    #Проверка наличия результатов
    assert "Кафедра информационной безопасности" in browser.title, "Не найден заголовок"
    browser.quit()


def test_menu_link(browser, wait):
    browser.get("https://www.fa.ru/")
    menu_button_xpath='//button[@class="burger-menu"]' #Локатор для кнопки меню

    wait.until(
        EC.presence_of_element_located((By.XPATH, menu_button_xpath))
    )
    #Получение объекта кнопки и клик по ней
    menu_button=browser.find_element(By.XPATH, menu_button_xpath)
    menu_button.click()

    #Локатор кнопки "Университет"
    university_button_xpath = '//div[@class="menu-tabs__item"]/button[text()="Университет"]'
    wait.until(
        EC.presence_of_element_located((By.XPATH, university_button_xpath))
    )
    university_button = browser.find_element(By.XPATH, university_button_xpath + '/..//a')
    #Получение атрибута "href" (ссылка) из кнопки "Университета"
    university_button_link = university_button.get_attribute("href")
    assert university_button_link== 'https://www.fa.ru/university/',"Неправильная ссылка в кнопке"

def test_itog(browser, wait):
    browser.get("https://www.fa.ru/") #открываем браузер
    search_button_xpath = '//button[@class="header__link _tooltip js-search-popup-toggle"]' #локатор кнопки
    wait.until(
        EC.element_to_be_clickable((By.XPATH, search_button_xpath))
    )
    search_button = browser.find_element(By.XPATH, search_button_xpath)
    search_button.click()
    input_area_xpath = '//input[@class="ui-field__input"]'  #локатор поля
    input_area = wait.until(
        EC.presence_of_element_located((By.XPATH, input_area_xpath))
    )
    search_text = "Кафедра информационной безопасности"
    input_area.clear()
    input_area.send_keys(search_text) #ввели текст
    search_button2_xpath = '//button[@class="ui-button _primary"]'
    wait.until(
        EC.element_to_be_clickable((By.XPATH, search_button2_xpath)))
    search_button2 = browser.find_element(By.XPATH, search_button2_xpath)
    search_button2.click()
    text = 'Найдено 100 результатов'
    wait.until(EC.presence_of_element_located((By.XPATH, f'//p[text()="{text}"]')))
