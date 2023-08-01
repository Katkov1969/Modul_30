import chromedriver_autoinstaller

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('/Users/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   pytest.driver.maximize_window()

   yield

   pytest.driver.quit()


def test_show_my_pets():
   #Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
      # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys(valid_email)

   # Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   #Переходим на вкладку Мои питомцы
   #Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

   #ТЕСТ ПРОВЕРКА КАРТОЧЕК ПИТОМЦЕВ

   # список всех обьектов питомца, в котром есть атрибут ".text" с помощью которого,
   # можно получить информацию о питомце в виде строки: 'Имя порода возраст'

   #Установка неявного ожидания
   #pytest.driver.implicity_wait(10)

   all_my_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

   # этот список image объектов , который имееют метод get_attribute('src') ,
   # благодаря которому можно посмотреть есть ли изображение питомца или нет.

   all_pets_images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')
   number_photo = len(all_pets_images)

   # проверяем что список своих питомцев не пуст
   assert len(all_my_pets) > 0

   #Получаем количество питомцев в таблице
   number_pets = len(all_my_pets)

   #Получаем количество питомцев из статистики
   count = pytest.driver.find_element(By.CLASS_NAME, 'task3').text
   count = count.split("\n")[1]
   count = count.split(" ")[-1]
   count = int(count)

   assert  number_pets == count


   #ТЕСТ ПРОВЕРКА ТАБЛИЦЫ ПИТОМЦЕВ
   pets_info = []
   for i in range(len(all_my_pets)):
      # получаем информацию о питомце из списка всех своих питомцев
      pet_info = all_my_pets[i].text

      # избавляемся от лишних символов '\n×'
      pet_info = pet_info.split("\n")[0]

      # добавляем в список pets_info информацию рода: имя, тип, возраст,  по каждому питомцу
      pets_info.append(pet_info)



   #Проверяем, что фото есть у более чем половины питомцев
   assert number_photo >= (number_pets / 2)


















