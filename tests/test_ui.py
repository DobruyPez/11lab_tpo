import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = Options()
    # КРИТИЧЕСКИ ВАЖНО для GitHub Actions:
    options.add_argument("--headless=new")  # headless режим
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    # Правильный путь к index.html
    index_path = os.path.abspath("index.html")
    driver.get(f"file://{index_path}")
    
    yield driver
    driver.quit()

def test_page_title(driver):
    assert "Форма обратной связи" in driver.title

def test_name_field_exists(driver):
    name_field = driver.find_element(By.ID, "name")
    assert name_field.is_displayed()

def test_email_field_exists(driver):
    email_field = driver.find_element(By.ID, "email")
    assert email_field.is_displayed()

def test_message_field_exists(driver):
    msg_field = driver.find_element(By.ID, "message")
    assert msg_field.is_displayed()

def test_submit_button_works(driver):
    driver.find_element(By.ID, "name").send_keys("Тест")
    driver.find_element(By.ID, "email").send_keys("test@test.com")
    driver.find_element(By.ID, "message").send_keys("Привет")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    response = driver.find_element(By.ID, "response").text
    assert "Спасибо, Тест!" in response