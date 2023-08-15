import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv


agent = UserAgent().random
headers = {
    "agent":agent
}
def search_and_save():
    result = ""
    #получаем данные на вход
    search = input("Введите запрос: ")
    pages = int(input("Введите количество страниц(1-25): "))
    base_url = f"https://www.olx.ua/uk/list/q-{search}/"
    #создаем таблицу с заголовками
    with open(f"data/{search}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(("page","number","name","price","url"))

    #парсим данные
    for page_number in range(1,pages+1):
        url =f"{base_url}?page={page_number}"
        req = requests.get(url, headers=headers)
        res = req.content
        soup = BeautifulSoup(res, "lxml")
        data = soup.find(class_ = "css-oukcj3").find_all(class_="css-1sw7q4x")
        allcount = len(data)
        print(f"Страница #{page_number}")
        result += f"Страница #{page_number}"
        count = 1
        for item in data:
            name = item.find(class_ = "css-16v5mdi er34gjf0").text
            if item.find(class_="css-10b0gli er34gjf0") != None:
                price = item.find(class_="css-10b0gli er34gjf0").text
            else:
                continue

            url = "https://www.olx.ua/" + item.find(class_="css-rc5s2u").get("href")
            print(f"{count} из {allcount}\n{name}\n{price}\n{url}\n")
            result += f"\n{count} из {allcount}\n{name}\n{price}\n{url}\n"
            #сохраняем рузультат в таблицу
            with open(f"data/{search}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerow((page_number, count, name.replace(","," "), price, url))
            if count == allcount:
                break
            count += 1
    #сохраняем результат в .txt
    with open(f"data/{search}.txt","w",encoding="utf-8") as file:
        file.write(result)

if __name__ == "__main__":
    search_and_save()
