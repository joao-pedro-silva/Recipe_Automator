import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from variables import username, password, delay, url
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class RecipeAutomator:
    def __init__(self, url, headers):

        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        #Get ingredients list from Gousto
        ingredients = soup.find_all('figcaption', {'class': 'indivrecipe-ingredients-text'})

        #List of ingredients
        self.ingredients_list = []
        quantity_list = []

        for a in ingredients:
            a = str(a.text.strip())
            #Add uncleaned ingredient to quantity_list
            quantity_list.append(a)

            #Clean ingredient
            a = ''.join(i for i in a if not i.isdigit())
            a = a.replace("(g)", "")
            a = a.replace("(ml)", "")
            a = a.replace("g ", "")
            a = a.replace("tsp ", "")
            a = a.replace("/", "")
            a = a.replace("†", "")

            #Add clean ingredient to ingredients_list
            self.ingredients_list.append(a)

        print(self.ingredients_list)
        print(quantity_list)

    def tesco_search(self, username, password):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.fullscreen_window()

        #Login and go to Grocereis
        self.driver.get("https://www.tesco.com/")
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/header/div/div[1]/ul/li[1]/div/a/span[2]") \
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]") \
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]") \
            .send_keys(password)
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[2]/div/form/button') \
            .click()
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/nav/div[1]/ul/li[1]/div/div[1]/a') \
            .click()
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/nav/div[1]/ul/li[1]/div/div[1]/div/div[2]/div[1]/ul/li[2]/a/h3/span') \
            .click()
        sleep(2)

        #ingredients_link = []

        for ingredient in self.ingredients_list:
            #Search for ingredient
            search_box = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/header/div[1]/div[2]/div/form/input[1]")
            search_box.send_keys(ingredient)
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/header/div[1]/div[2]/div/form/button') \
                .click()

            #Time for user to add deseried item to cart
            sleep(delay)

            #ingredients_link.append(self.driver.current_url)

            self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/header/div[1]/div[2]/div/form/input[1]").click()

        #print(ingredients_link)

user_agent = ''
headers = {"User-Agent": user_agent}

my_bot = RecipeAutomator(url, headers)
my_bot.tesco_search(username, password)
