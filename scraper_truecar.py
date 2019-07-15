# creates a csv file and a sql file for 'truecar.com'

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import csv
import sqlite3

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

def standard_len(car_list):
    difference = 1
    while difference != 0:
        length = len(car_list)
        for row in car_list:
            if len(row) != 7:
                print(row)
                car_list.remove(row)
        difference = length - len(car_list)
    return car_list

def create_csv(csv_name, car_list):
    with open(csv_name,'w',newline='') as csvfile:
        carwriter = csv.writer(csvfile, delimiter = ',')
        for car in car_list:
            carwriter.writerow(car)

def create_sql(sql_name, car_list):
    conn = sqlite3.connect('cars.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE cars
                (Year integer, Make text, Model text, Trim text, Drive text, Mileage integer, Price Integer)''')
    c.executemany('INSERT INTO cars VALUES (?,?,?,?,?,?,?)', car_list)            
    conn.commit()
    
url = 'https://www.truecar.com/used-cars-for-sale/listings/ford/edge/location-charlottesville-va/?searchRadius=500'

car_list = make_complete_list(url)
car_list = standard_len(car_list)


csv_name = 'test.csv'
sql_name = 'test.sqlite'

create_csv(csv_name, car_list)
create_sql(sql_name, car_list)