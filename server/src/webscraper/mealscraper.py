"""
    This module contains the class NutritionScraper which is used to scrape nutritional information 
    from the UCSC website
"""
import re
import datetime
import json
import requests
import urllib3
import food
from tqdm import tqdm

class MealScraper():
    """This class provides functions to scrape the nutritional information from the UCSC dining website"""
    linkPrefix = "https://nutrition.sa.ucsc.edu/"
    mainLink = "https://nutrition.sa.ucsc.edu/longmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=40&locationName="
    datePrefix = "&naFlag=1&WeeksMenus=UCSC+-+This+Week%27s+Menus&dtdate="
    # dates
    
    def __init__(self, location_name: str, meal_num: int, month: int, day: int, year :int):
        urllib3.disable_warnings()
        self.location_name = location_name
        self.mealsByLocation = {"John R. Lewis Dining Hall & College Nine Dining Hall": ["Breakfast", "Lunch", "Dinner", "Late+Night"],
        "Cowell & Stevenson Dining Hall": ["Breakfast", "Lunch", "Dinner", "Late+Night"],
        "Crown & Merrill Dining Hall and Banana Joe's": ["Breakfast", "Lunch", "Dinner", "Late+Night"],
        "Porter & Kresge Dining Hall": ["Breakfast", "Lunch", "Dinner"],
        "Rachel Carson & Oakes Dining Hall": ["Breakfast", "Lunch", "Dinner", "Late+Night"],
        "Oakes Cafe": ["Breakfast", "All+Day"],
        "Global Village Cafe": ["Menu"],
        "Owl's Nest Cafe": ["Breakfast", 'All'],
        "Slug Stop": ["Menu"],
        "UCen Bistro": ["Menu"],
        "Stevenson Coffee House": ["Menu"]}
        self.meal = self.mealsByLocation[location_name][meal_num] # gets inputted meal
        self.monthString = str(month) + "%2f" # gets month
        self.dayString = str(day) + "%2f" # gets day
        self.yearString = str(year) + "&mealName=" # gets year


    # header to be used for scraping
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

    def get_main_link(self):
        """Returns link to main nutrition website"""
        return ( self.mainLink +
                self.get_dining_hall_link(self.location_name) +
                self.datePrefix +
                self.monthString +
                self.dayString +
                self.yearString +
                self.meal )

    def get_dining_hall_link(self, name: str):
        """Converts Dining Hall name into URL form"""
        s = ""
        words = name.split()
        for word in words:
            match word:
                case "&":
                    s += "%26"
                case _:
                    s += word
            s += "+"
        return s[:len(s)-1]

    def get_line_nums_of_categories(self, file_name: str):
        """Gets each food category and the respective line number and 
        returns it as a tuple containing two lists"""
        
        with open(file_name, "r") as file:
            html_string = file.read()
        categories = re.findall(r"--\s*(?!.*\b(Aurora|aspx)\b)(.*?)\s*--", html_string)
        target_strings = []
        line_nums = []
        for tuple in categories:    
            target_strings.append(tuple[1])  
        with open(file_name, 'r') as file:
            for line_number, line in enumerate(file, 1):
                for target_string in target_strings:
                    formatted_string = "-- " + target_string + " --"
                    if formatted_string in line: 
                        line_nums.append(line_number)
        return dict(zip(line_nums, target_strings))
    
    def append_food_to_category(self, line_num_dict: dict, food, food_line_num: int, category_dict: dict):
        prev_line_num = None
        for line_num in sorted(line_num_dict.keys()):  # Ensure the line numbers are sorted
            if food_line_num > line_num:
                prev_line_num = line_num
            else:
                break  # Stop at the first line number greater than food_line_num

        if prev_line_num is not None:
            category_dict[line_num_dict[prev_line_num]].append(food)

    
    def get_line_num_of_food(self, food_name: str, file_name: str):
        with open(file_name, 'r') as file:
            for line_number, line in enumerate(file, 1):
                formatted_name = '>' + food_name + '<'
                if formatted_name in line: 
                    return(line_number)
    
    def create_category_dict(self, line_num_dict: dict):
        """Creates a dictionary where the keys are the categories of food and 
        the pairs are empty lists
        
        Args:
            line_num_dict: dictionary where the keys are line numbers and 
            the values are the corresponding food. To be passed in from get_line_nums_of_categories
            
        Returns:
            A dictionary where the keys are categories of food and the values are empty lists"""
        category_dict = {}
        for line_num in line_num_dict:
            category_dict[line_num_dict[line_num]] = []
        return category_dict
    
    def get_clean_header(self, input_str: str):
        """Converts headerString into a dictionary"""
        header_list = [list(rowString.split(": ")) for rowString in input_str.split("\n")]
        headers = {x[0].strip():x[1].strip() for x in header_list}
        return headers
    
    def find_macronutrient(self, response: str, nutrient_name: str):
        """Returns the amount of a specified nutrient
        
        Args:
            response: The text from the scraped nutrition label.
            nutrient_name: The name of the nutrient which will be found.
        
        Returns:
            A string containing the amount of the given macronutrient.
        """
        # gets index of the nutrient
        find_index = response.find(nutrient_name)
        # gets substring containing nutrient info
        nutrient_string = response[find_index:find_index + 100]
        # gets index of end of nutrient amount
        find_index_2 = nutrient_string.find("g")
        # finds index of start of nutrient amount
        i = find_index_2
        while True:
            if nutrient_string[i:i+1] == ">":
                i += 1
                break
            if nutrient_string[i:i+1] == "-":
                return "0"
            i -= 1
            if i == 0:
                break
        return_str = nutrient_string[i:find_index_2]
        # checks if nutrient is in milligrams or grams
        if return_str[len(return_str)-1:] == "m":
            return return_str
        return return_str

    # returns number of calories in nutrition label
    def get_calories(self, response: str):
        """Returns a string with the amount of calories on the given nutrition label
        
        Args:
            response: The text from the scraped nutrition label.
        Returns:
            A string containing the amount of calories on the given nutrition label
        """
        find_index_calories = response.find("Calories")
        calorie_string = response[find_index_calories:find_index_calories+100]
        find_index_2 = calorie_string.find("p;")
        i = find_index_2 + 2
        while True:
            if calorie_string[i:i+1] == "<":
                break
            i += 1
            if i == 1000:
                break
        return calorie_string[find_index_2+2:i]
    
    def convert_nutrition_to_object(self, names: list, nutrition_list: list) -> list:
        foods = []
        for i in range(len(names)):
            calories = nutrition_list[i]["Calories"]
            total_fat = nutrition_list[i]["Total Fat"]
            total_carbs = nutrition_list[i]["Tot. Carb."]
            protein = nutrition_list[i]["Protein"]
            curr = food.Food(names[i],calories, total_fat, total_carbs, protein)
            foods.append(curr)
        return foods
        
    def convert_food_dict_to_json_dumpable(self, food_dict: dict, line_num_dict):
        json_dumpable = self.create_category_dict(line_num_dict)
        for category in food_dict:
            for food in food_dict[category]:
                json_dumpable[category].append(food.dict_form)
        return json_dumpable


    # returns dictionary of macronutrients and the amount of said macronutrient
    def get_all_macros(self, response: str):
        """Returns dictionary containing the macronutrients of a given nutrition label"""
        macro_list = ["Total Fat", "Tot. Carb.", "Protein"]
        macros = {}
        macros["Calories"] = float(self.get_calories(response))
        for macro in macro_list:
            macros[macro] = float(self.find_macronutrient(response,macro))
        return macros

    def add_prefix(self, string: str):
        """Returns a string with the link prefix prepended to the given string"""
        return self.linkPrefix + string
    
    def scrape_nutrition(self):
        """Scrapes the nutritional info of a given time period from a given UCSC dining hall 
        and dumps the result into a JSON
        """
        headers = self.get_clean_header(self.headerString)
        response_main = requests.get(self.get_main_link(), headers=headers, verify=False, timeout=2)
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(response_main.text)
            print(response_main.headers)
        with open("output.html", "r", encoding="utf-8") as f:
            html_string = f.read()
        
        category_line_nums = self.get_line_nums_of_categories("output.html")
        
        # regex pattern to pull links from file
        link_pattern = r"'(label\.aspx\?[^']*)\'"
        # regex pattern to pull food names from file
        name_pattern = r"';\">([^<]+)</a>"
        
        # gets all names of foods from selected dining hall
        names = list(re.findall(name_pattern, html_string))
        
        # gets links to nutrition labels of foods
        links = list(re.findall(link_pattern, html_string))
        links = list(map(self.add_prefix, links))
        nutrition_list = []
        
        # loop over each nutrition label to scrape info
        for i in tqdm (range(len(links)), desc="Scraping Nutrition..."):
            response = requests.get(links[i], headers=headers, verify=False, timeout=5)
            nutrition_info = self.get_all_macros(response.text)
            nutrition_list.append(nutrition_info)
        
        nutrition_dict = dict(zip(names,nutrition_list))
        
        if len(nutrition_dict) == 0:
            print("Error, dictionary empty")
        else:
            print("Success!")
        
        category_dict = self.create_category_dict(category_line_nums)
        food_objects = self.convert_nutrition_to_object(names, nutrition_list)
        
        for food in food_objects:
            food_line_num = self.get_line_num_of_food(food.name, "output.html")
            self.append_food_to_category(category_line_nums, food=food, food_line_num=food_line_num, category_dict=category_dict)
            
        # writes results to json file
        with open("nutritionInfo.json", "w", encoding="utf-8") as f:
            json.dump(self.convert_food_dict_to_json_dumpable(category_dict, category_line_nums), f, indent=4)
