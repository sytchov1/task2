import feedparser
import numpy
import re
from wordcloud import WordCloud, STOPWORDS
from PIL import Image


# Url запроса с сайта Google News по ключевому слову Russia за последние 30 дней
RSS_URL = 'https://news.google.com/rss/search?q=Russia%20when%3A30d&hl=en-US&gl=US&ceid=US%3Aen'


# Данная функция парсит rss-структуру, собирая заголовки статей, и чистит полученных текст от знаков пунктуации
def getData(url):
    result = []

    feed = feedparser.parse(url)
    for newsitem in feed['items']:
        title = newsitem['title'][:-3 - len(newsitem['source']['title'])]
        result.append(re.sub(r'[^a-zA-Z\s]', '', title))
    return ' '.join(result).upper()


# Данная функция создаёт Word Cloud изображение на основе полученных данных и выбирает 50 наиболее встречаемых
# Слова по типу 'i', 'me', 'my', 'myself', 'we' и т.д. отсекаются
# Для работы необходимо наличие в фолдере с данным скриптом изображения cloud.png
# Полученное изображение будет помещено в фолдер со скриптом
def createCloud(data):
    mask = numpy.array(Image.open("cloud.png"))
    mask[mask == 0] = 255
    cloud = WordCloud(background_color="white", max_words=50, mask=mask, stopwords=set(STOPWORDS))
    cloud.generate(data)
    cloud.to_file("wordCloud.png")


def main():
    data = getData(RSS_URL)
    createCloud(data)


if __name__ == '__main__':
    main()
