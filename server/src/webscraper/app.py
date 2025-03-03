from typing import Union
from fastapi import FastAPI
import json
import mealscraper

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/locations")
def read_locations():
    return {"locations": ["jrlc9-dh", "cs-dh", "cm-dh", "pk-dh", "rcco-dh"]}

@app.get("/meals/{dining_hall_name}_{date}")
def read_meals(dining_hall_name: str, date: str):
    return {"breakfast": True,
            "lunch": True}
    
@app.get("/categories/{dining_hall_name}_{date}_{meal}")
def read_categories(dining_hall_name: str, date: str, meal :str):
    with open(dining_hall_name + "_" + date + "_" + meal + ".json", "r", encoding="utf-8") as f:
        meal_info = json.load(f)
    category_list = [category for category in meal_info]
    return category_list

@app.get("/{dining_hall_name}_{date}_{meal}")
def read_meal(dining_hall_name: str, date: str, meal :str):
    with open(dining_hall_name + "_" + date + "_" + meal + ".json", "r", encoding="utf-8") as f:
        meal_info = json.load(f)
    return meal_info

