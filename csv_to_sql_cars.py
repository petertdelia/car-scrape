import csv
import sqlite3

# import car list
car_list =[]
with open('ford_edge.csv', newline = '') as csvfile:
    carreader = csv.reader(csvfile)
    for row in carreader:
        car_list.append(row)

# for Ford Edges, ensuring that the data is the correct length

difference = 1
while difference != 0:
    length = len(car_list)
    for row in car_list:
        if len(row) != 7:
            print(row)
            car_list.remove(row)
    difference = length - len(car_list)

for i in range(len(car_list)):
    car_list[i] = tuple(car_list[i])



conn = sqlite3.connect('cars.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE cars
            (Year integer, Make text, Model text, Trim text, Drive text, Mileage integer, Price Integer)''')
conn.commit()

