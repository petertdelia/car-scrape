# using selenium for 'truecar.com'

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

def get_site(url):
    driver = webdriver.Firefox()
    driver.get(url)
    return driver

def make_soup(driver):
    soup = BeautifulSoup(driver.page_source)
    return soup

def init_car_list():
    car_list = []
    return car_list

def populate_temp_car_list(soup):
    titles = soup.findAll("h4",{"data-test":"vehicleListingCardTitle"})
    temp_car_list = []
    for title in titles:
        temp_car_list.append(title.text.split())
    mileages = soup.findAll("div",{"data-test":"vehicle-listing-mileage"})
    i = 0
    for mileage in mileages:
        mileage=mileage.text.split()[1].replace(',','')
        temp_car_list[i].append(mileage)
        i+=1
    prices = soup.findAll("h4",{"data-test":"vehicleListingPriceAmount"})
    i = 0
    for price in prices:
        price = price.text.replace('$','').replace(',','')
        temp_car_list[i].append(price)
        i+=1
    return temp_car_list


def extend_car_list(car_list,temp_car_list):
    car_list.extend(temp_car_list)
    print(len(car_list))
    return car_list

def go_to_next_page(driver):
    try:
        element = driver.find_element_by_css_selector('[data-test=Pagination-directional-next]')
        element.click()
        return True
    except:
        print('all done!')
        return False

def make_complete_list(url):
    driver = get_site(url)
    car_list = init_car_list()
    input("Press Enter to continue...")
    flag = True
    while (flag == True):
        sleep(1)
        soup = make_soup(driver)
        temp_car_list = populate_temp_car_list(soup)
        car_list = extend_car_list(temp_car_list,car_list)
        flag = go_to_next_page(driver)
    driver.close()
    return car_list