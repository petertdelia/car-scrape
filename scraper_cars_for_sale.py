# works for 'carsforsale.com'

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from time import sleep

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
    # this list initialization and for loop could be better organized
    temp_car_list = [[] for i in range(len(name_containers))]
    i=0
    for index in name_containers:  
        name = name_containers[i].h4.text  
        temp_car_list[i] = name.split()
        i+=1
    # add mileages
    mileages = soup.findAll("div",{"class":"specs-miles"})
    for i in range(len(mileages)): 
        mileages[i] = mileages[i].text.split()
        mileage = mileages[i]
        mileages[i] = mileage[0].replace(',','')
        try:
            temp_car_list[i].append(mileages[i])
        except IndexError:
            print('index out of range--oops!')
    # add features (only AWD/FWD for now)
    feat_containers = soup.findAll("ul", {"class":"specs"})
    features = []
    for feat in feat_containers[2::3]:
        feat = feat.text
        if (feat.find('AWD') != -1):
            feat = 'AWD'
        else:
            feat = 'FWD'
        features.append(feat)
    for i in range(len(features)):
        temp_car_list[i].append(features[i])
    # add prices
    price_containers = soup.findAll("li", {"class":"vehicle-price"})
    prices = []
    for price in price_containers[0::2]:  
        price = price.text.strip()
        if (len(price) > 9):
            price = price[0:8]
        price = price.replace(',','').replace('$','')
        prices.append(price)
    for i in range(len(prices)):
        temp_car_list[i].append(prices[i])
    print(temp_car_list[0])
    return temp_car_list

def append_to_car_list(temp_car_list,car_list):
    car_list.extend(temp_car_list)
    print(len(car_list))
    return car_list

def go_to_next_page(driver):
    try:
        element = driver.find_element_by_css_selector('button.btn-pagination-next')
        element.click()
        return True
    except:
        print('an error occurred when clicking to the next page')
        return False

# all ford edges
# url = 'https://www.carsforsale.com/Search?Make=Ford&Model=Edge&Conditions=used&PageNumber=1&OrderBy=Relevance&OrderDirection=Desc'

# 2015 ford edges
# url = 'https://www.carsforsale.com/Search?SearchTypeID=2&Make=Ford&Model=Edge&BodyStyle=&SubBodyStyle=&MinModelYear=2015&MaxModelYear=2015&MinPrice=&MaxPrice=&FromEstimatedMonthlyPayment=&ToEstimatedMonthlyPayment=&MaxMileage=&FromFuelEconomy=&Radius=&ZipCode=&State=&City=&FullStateName=&Latitude=&Longitude=&Conditions=Used&Conditions=Manufacturer+Certified&Conditions=Repairable&HideRepairable=&FilterImageless=&PricedVehiclesOnly=&OrderBy=Relevance&OrderDirection=desc&PageResultSize=15&PageNumber=1&TotalRecords=&FromDate=&ToDate=&DaysListed=&SourceId=&SourceExternalUserID='

# 2015 ford edges near 22903
url = 'https://www.carsforsale.com/Search?SearchTypeID=2&Make=Ford&Model=Edge&BodyStyle=&SubBodyStyle=&MinModelYear=2015&MaxModelYear=2015&MinPrice=&MaxPrice=&FromEstimatedMonthlyPayment=&ToEstimatedMonthlyPayment=&MaxMileage=&FromFuelEconomy=&Radius=100&ZipCode=22903&State=&City=&FullStateName=&Latitude=&Longitude=&Conditions=Used&Conditions=Manufacturer+Certified&Conditions=Repairable&HideRepairable=&FilterImageless=&PricedVehiclesOnly=&OrderBy=Relevance&OrderDirection=desc&PageResultSize=15&PageNumber=1&TotalRecords=&FromDate=&ToDate=&DaysListed=&SourceId=&SourceExternalUserID='

def make_complete_list(url):
    driver = get_site(url)
    car_list = init_car_list()
    flag = True
    while (flag == True):
        sleep(1)
        soup = make_soup(driver)
        temp_car_list = populate_temp_car_list(soup)
        car_list = append_to_car_list(temp_car_list,car_list)
        flag = go_to_next_page(driver)
    driver.close()
    return car_list


car_list = make_complete_list(url)

# make a pandas dataframe using the car list
from pandas import DataFrame
df = DataFrame.from_records(car_list, columns=['year', 'make', 'model', 'trim', 'mileage', 'AWD/FWD', 'price'])
# strip whitespace
df = df.apply(lambda x: x.str.strip())
# save to csv
df.to_csv('df_cars.csv')

# do some data cleaning
df['price'] = pd.to_numeric(df['price'])



# save to csv file
headers = 'year, make, model, trim, mileage, AWD/FWD, price\n'
with open('cars.csv', 'w') as f:
    f.write(headers)
    for car in car_list:
        f.write(str(car).strip('[]').replace("'",''))
        f.write('\n')
