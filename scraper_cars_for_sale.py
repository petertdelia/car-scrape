# works for 'carsforsale.com'

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

from bs4 import BeautifulSoup

def get_site(url):
    driver = webdriver.Firefox()
    driver.get(url)
    return driver

def make_soup(driver):
    soup = BeautifulSoup(driver.page_source,features="html.parser")
    return soup

def init_car_list():
    car_list = []
    return car_list

def populate_temp_car_list(soup):
    name_containers = soup.findAll("a", {"class":"vehicle-name"})
    temp_car_list = [[] for i in range(len(name_containers))]
    i=0
    for index in name_containers:  
        name = name_containers[i].h4.text  
        temp_car_list[i] = name.split()
        i+=1
    mileages = soup.findAll("div",{"class":"specs-miles"})
    for i in range(len(mileages)): 
        mileages[i] = mileages[i].text.split()
        mileage = mileages[i]
        mileages[i] = mileage[0]
        try:
            temp_car_list[i].append(mileages[i])
        except IndexError:
            print('index out of range--oops!')
    return temp_car_list

def append_to_car_list(temp_car_list,car_list):
    car_list.extend(temp_car_list)
    print(len(car_list))
    return car_list

def go_to_next_page(driver):
    try:
        element = driver.find_element_by_css_selector('button.btn-pagination-next')
        element.click()
    except:
        print('an error occurred when clicking to the next page')

url = 'https://www.carsforsale.com/Search?Make=Ford&Model=Edge&Conditions=used&PageNumber=1&OrderBy=Relevance&OrderDirection=Desc'

def put_it_together():
    driver = get_site(url)
    soup = make_soup(driver)
    car_list = init_car_list()
    temp_car_list = populate_temp_car_list(soup)
    car_list = append_to_car_list(temp_car_list,car_list)
    go_to_next_page(driver)
    driver.close()

put_it_together()
