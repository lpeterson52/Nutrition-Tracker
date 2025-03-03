"""Main Method"""

import mealscraper
import food

def main():
    """Main method"""

    scraper = mealscraper.MealScraper(location_name="John R. Lewis Dining Hall & College Nine Dining Hall", 
                                      meal_num=1, 
                                      month=3, 
                                      day=2, 
                                      year=2025)
    scraper.scrape_nutrition()

if __name__ == "__main__":
    main()
