import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from dateutil import parser

def get_pages(event_table_url) -> list:
    domain = "https://" + urlparse(event_table_url).netloc

    page = requests.get(event_table_url)
    print(event_table_url)
    soup = BeautifulSoup(page.content, "html.parser")
    tile_elements = soup.find_all("div", class_="new-tile")
    pages = []

    for tile_element in tile_elements:
        event_url = domain + tile_element.find("a")["href"]
        pages.append(EventPage(event_url))

    return pages


class EventPage:
    def __init__(self, url):
        self.url = url
        self.title = "[empty]"
        self.type = ""
        self.length = ""
        self.genres = ""
        self.link_trailer = ""
        self.times = ""

    def __iter__(self):
        return iter([
            self.url,
            self.title,
            self.type,
            self.length,
            self.genres,
            self.times,
            self.link_trailer,
        ])

    def parse(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        self.title = soup.find("h1").text

        type_matches = re.compile("[A-Za-z ]+").search(soup.find_all("h4")[1::1][0].text)

        if type_matches:
            self.type = type_matches.group(0)

        try:
            self.length = soup.find("div", class_="facts").find_all("p")[2::2][0].text
        except:
            self.length = "-"
        # Das iframe existiert erst wenn man den Cookies zugestimmt hat.
        # Da ich das gerade nicht programmiert bekomme, lasse ich den Trailer mal weg.
        #self.link_trailer = soup.find("iframe").attrs["src"]

        try:
            genres_tag_list = soup.find("h3", class_="tags").find_all("span")

            for genres_tag in genres_tag_list:
                self.genres += genres_tag.text + ","
        except:
            self.genres = "-"


        stagings = soup.find_all("div", class_="staging")

        # get start times
        for staging in stagings:
            ics_link = staging.find("a")
            m = re.compile("(?<=DTSTART;TZID=Europe/Berlin:)[0-9]+T[0-9]+").search(str(ics_link))

            if m:
                self.times += str(parser.parse(m.group(0))) + "\n"

