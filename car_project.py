import mysql.connector
import requests
from bs4 import BeautifulSoup
import re
import datetime


### connecting to DB##

connection_args = {
    'host': 'localhost',
    'database': 'khodro',
    'user': 'root',
    'password': '**',
    'port': '3308'
}

cnx = mysql.connector.connect(**connection_args)

mycursor = cnx.cursor()

#### geting information from website###

r = requests.get(r'https://bama.ir/car/renault-tondar90?priced=1')
soup = BeautifulSoup(r.text, 'html')
val = soup.find_all('a', attrs={'title': 'رنو، تندر 90'})
print(len(val))
# print(val)

for i, link in enumerate(soup.find_all('a', attrs={'title': 'رنو، تندر 90'})):
    # for i in val:
    # cars model

    model = val[i].find('div', attrs={'class': 'bama-ad__detail-row'})
    paragraphs = str(model)
    # Model = int(re.findall(r'>(\d{4}).*?/span>', paragraphs)[0])
    Model = int(re.findall(r'(\d{4})\n', paragraphs)[0])

# cars price

    price = val[i].find('div', attrs={'class': 'bama-ad__price-holder'})
    paragraphs = str(price)
    # Price = re.findall(r'>(\d.*?)</span>', paragraphs)[0]
    Price = re.findall(r'(\d.*,\d{3})\n', paragraphs)[0]

# Date

    x = datetime.datetime.now()
    ol = x.strftime('%Y-%m-%d %H:%M:%S')
    date_time_obj = datetime.datetime.strptime(ol, '%Y-%m-%d %H:%M:%S')

    mycursor.execute("INSERT INTO car VALUES (\'L90\', %s, %s , %s, DEFAULT)", [
                     Model, Price, date_time_obj])

    print(i)

    cnx.commit()
