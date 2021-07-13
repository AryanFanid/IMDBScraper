import requests
from bs4 import BeautifulSoup
import csv


url = 'https://www.imdb.com/list/ls016522954/'
header = ['#', 'Name', 'Year', 'Age Rating', 'Duration',
          'Genre', 'Rating', 'Description', 'Director(s)', 'Stars', 'Release Date']

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
movies = soup.find_all("div", class_='lister-item')

with open('moviesData.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for movie in movies:
        row = []
        row.append(movie.find(
            "span", class_="lister-item-index").text.rstrip('.'))
        row.append(movie.find("h3", class_="lister-item-header").find("a").text)
        row.append(movie.find("span", class_="lister-item-year").text)

        certificate = movie.find("span", class_="certificate")
        runtime = movie.find("span", class_="runtime")
        genre = movie.find("span", class_="genre")
        row.append(certificate.text) if certificate else row.append(None)
        row.append(runtime.text) if runtime else row.append(None)
        row.append(genre.text.replace('\n', '')) if genre else row.append(
            movie.find("b").text.replace('\n', ''))

        rating = movie.find("span", class_="ipl-rating-star__rating")
        row.append(rating.text) if rating else row.append(None)
        row.append(movie.find_all("p")[1].text.replace('\n', ''))

        DirectorsAndStars = movie.find_all(
            "p")[2].text.replace("\n", "").split("|")
        if len(DirectorsAndStars) == 1:
            row.append(None)
            item = DirectorsAndStars[0]
            row.append(item[item.find(':')+1:])
        else:
            for item in DirectorsAndStars:
                row.append(item[item.find(':')+1:].rstrip())
        row.append(movie.find("div", class_="list-description").find("b").text)

        writer.writerow(row)
