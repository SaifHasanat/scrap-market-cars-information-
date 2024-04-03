import csv, requests, lxml, time, pandas as pd, openpyxl
from bs4 import BeautifulSoup
from pathlib import Path
from random_user_agent import pick_random_useragent

path = Path.home() / Path('WebScraping', 'Scrap_souq', 'Cars.csv')
file = open(path, 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
headers = ['image', 'price', 'Car_Make', 'Model', 'Fuel', 'Transmission', 'Year', 'Condition', 'Kilometers', 'City',
           'Neighborhood', 'url']
writer.writerow(headers)

for page in range(5):
    if page == 0:
        url = 'https://jo.opensooq.com/en/cars/cars-for-sale'
    else:
        url = f'https://jo.opensooq.com/en/cars/cars-for-sale?search=true&page={page}'

    user_agent = pick_random_useragent()
    headers = {'User_Agent': user_agent}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        a_elements = soup.find_all('a', class_='block blackColor p-16')
        add_url = 'https://jo.opensooq.com'
        cards_urls = [add_url + a.get('href') for a in a_elements]
        for url in cards_urls:
            try:
                re = requests.get(url, headers=headers)
                time.sleep(3)
                if re.status_code == 200:
                    soup = BeautifulSoup(re.text, 'lxml')
                    try:
                        image = soup.find('div', class_='image-gallery-slide center').find("img").get('src')
                    except Exception as e:
                        image = 'None'
                        print(e)

                    try:
                        price = soup.find('div',
                                          class_='flex alignItems relative priceColor bold font-30 width-fit').text
                    except Exception as e:
                        price = 'None'
                        print(e)

                    try:
                        Condition = soup.find('a', class_='bold blackColor Condition').text
                    except Exception as e:
                        Condition = 'None'
                        print(e)

                    try:
                        Year = soup.find('a', class_='bold blackColor Year').text
                    except Exception as e:
                        Year = 'None'
                        print(e)

                    try:
                        Kilometers = soup.find('a', class_='bold blackColor Kilometers').text
                    except Exception as e:
                        Kilometers = 'None'
                        print(e)

                    try:
                        Fuel = soup.find('a', class_='bold blackColor Fuel').text
                    except Exception as e:
                        Fuel = 'None'
                        print(e)

                    try:
                        City = soup.find('a', class_='bold blackColor City').text
                    except Exception as e:
                        City = 'None'
                        print(e)

                    try:
                        Neighborhood = soup.find('a', class_='bold blackColor Neighborhood').text
                    except Exception as e:
                        Neighborhood = 'None'
                        print(e)

                    try:
                        Car_Make = soup.find('a', class_='bold blackColor Car Make').text
                    except Exception as e:
                        Car_Make = 'None'
                        print(e)

                    try:
                        Transmission = soup.find('a', class_='bold blackColor Transmission').text
                    except Exception as e:
                        Transmission = 'None'
                        print(e)

                    try:
                        Model = soup.find('a', class_='bold blackColor Model').text
                    except Exception as e:
                        Model = 'None'
                        print(e)

                    writer.writerow(
                        [image, price, Car_Make, Model, Fuel, Transmission, Year, Condition, Kilometers, City,
                         Neighborhood, url])
            except Exception as e:
                print(e)


def convert_to_excel(my_file):
    df = pd.read_csv(my_file)
    df.to_excel(f'data/{my_file}.xlsx', index=False)
