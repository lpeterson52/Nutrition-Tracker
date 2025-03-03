"""
This module contains a class for a webscraper which scrapes what meals are available at each location in UCSC
"""

import re
import datetime
import json
import requests
import urllib3
import food
from tqdm import tqdm

class ScrapeByLocation:
    
    OUTPUT_PATH = "server/src/webscraper/meal_output.html"
    def __init__(self):
        pass
    
    
    headerString = """
    accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    accept-encoding: gzip, deflate, br, zstd
    accept-language: en-US,en;q=0.9
    cache-control: max-age=0
    cookie: nmstat=dbc72b5e-467d-1d4c-4ec0-09407dd3af4e; _hjSessionUser_3860872=eyJpZCI6Ijc1MzFhMmI3LWZmNDUtNWQyOC05MmRjLWNmMGFmNDE3ZWNkNSIsImNyZWF0ZWQiOjE3MjA0Njk0NjAyODIsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.1876244345.1720334281; _ga_YSK09XHBWK=GS1.1.1727391092.1.0.1727391095.0.0.0; _ga_BWJ4Z4Y66X=GS1.1.1727406832.10.1.1727407016.0.0.0; _hp2_props.3001039959=%7B%22Base.appName%22%3A%22Canvas%22%7D; _hp2_id.3001039959=%7B%22userId%22%3A%225450010249110384%22%2C%22pageviewId%22%3A%225820543749153110%22%2C%22sessionId%22%3A%223224987423913875%22%2C%22identity%22%3A%22uu-2-3f7fe8885f071a3adb15c8d16cf7c5256e74604a83fdfeb8359e06ffd3bc86be-subopMsfCdn2dwy8anU0QwbgC2CqHbZFnJmMvElg%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; PS_DEVICEFEATURES=width:1512 height:982 pixelratio:2 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; WebInaCartDates=; WebInaCartMeals=; WebInaCartRecipes=; WebInaCartQtys=; WebInaCartLocation=40
    priority: u=0, i
    referer: https://nutrition.sa.ucsc.edu/shortmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=40&locationName=John+R.+Lewis+%26+College+Nine+Dining+Hall&naFlag=1
    sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "macOS"
    sec-fetch-dest: document
    sec-fetch-mode: navigate
    sec-fetch-site: same-origin
    sec-fetch-user: ?1
    upgrade-insecure-requests: 1
    user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
    """.strip()
    
    def get_clean_header(self, input_str: str):
        """Converts headerString into a dictionary"""
        header_list = [list(rowString.split(": ")) for rowString in input_str.split("\n")]
        headers = {x[0].strip():x[1].strip() for x in header_list}
        return headers

    def scrape_meals(self):
        headers = self.get_clean_header(self.headerString)
        response = requests.get("https://nutrition.sa.ucsc.edu/shortmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=40&locationName=John+R.+Lewis+%26+College+Nine+Dining+Hall&naFlag=1",
                     headers=headers,
                     verify=False,
                     timeout=2)
        with open(self.OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(response.text)
            print(response.headers)


if __name__ == "__main__":
    scraper = ScrapeByLocation()
    scraper.scrape_meals()
    