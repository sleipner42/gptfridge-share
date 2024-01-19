import scrapy
import json
from recipe_scrapers import BBCFood

class BBCSpider(scrapy.Spider):
    name = "bbc"
    
    PAGE_SIZE = 24
    TOTAL_COUNT = 6013

    def start_requests(self):

        urls = [
            f"https://www.bbc.co.uk/food/api/search?q=&chefs=&courses=light_meals_and_snacks,main_course&cuisines=&diets=&dishes=&occasions=&programmes=&quick=&inSeason=&page={n}"
            for
            n in range(1, self.TOTAL_COUNT // self.PAGE_SIZE + 1)
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        json_data = json.loads(response.text)

        for item in json_data['recipes']:
            yield response.follow(item['url'], self.parse_recipe)

    def parse_recipe(self, response):
        recipe = BBCFood(url=None, html=response.text)
        yield recipe.to_json()
