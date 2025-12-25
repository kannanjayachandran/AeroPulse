"""
Simple scraper using BeautifulSoup

    This is for educational purpose only

    All the data collected from Skytrax is the intellectual properties of `Skytrax` 
    and is collected by abiding with their terms and conditions. Please read their terms 
    and conditions before performing any sort of automated actions on their site or servers.
"""

import os
import requests
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AeroPulseBot/2.0)"}
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "Data/raw"
PAGES = 1
PAGE_SIZE = 1


def safe_text(el) -> Optional[str]:
    return el.get_text(strip=True) if el else None


def fetch_page_reviews(base_url: str, page: int, page_size: int):
    print(f"Scraping page {page}")
    url = f"{base_url}/page/{page}/?sortby=post_date%3ADesc&pagesize={page_size}"
    res = requests.get(url, headers=HEADERS, timeout=20)
    res.raise_for_status()

    soup = BeautifulSoup(res.content, "html.parser")

    reviews = []

    review_blocks = soup.find_all("article", itemprop="review")

    for block in review_blocks:
        try:
            record = {
                "review_id": None,
                "review_date": None,
                "flight_date": None,
                "route_origin": None,
                "route_destination": None,
                "aircraft_model": None,
                "seat_class": None,
                "traveler_type": None,
                "trip_verified_flag": None,
                "recommended_flag": None,
                "overall_rating_10": None,
                "seat_comfort_rating": None,
                "cabin_staff_rating": None,
                "food_beverage_rating": None,
                "ground_service_rating": None,
                "value_for_money_rating": None,
                "review_title": None,
                "review_text": None,
            }

            # review id
            for cls in block.get("class", []):
                if cls.startswith("review-"):
                    record["review_id"] = cls.replace("review-", "")
                    break

            # review date
            meta_date = block.find("meta", itemprop="datePublished")
            if meta_date:
                record["review_date"] = meta_date.get("content")

            # overall rating
            rating_el = block.find("div", class_="rating-10")
            if rating_el:
                val = rating_el.find("span", itemprop="ratingValue")
                if val:
                    record["overall_rating_10"] = int(val.text.strip())

            # title
            record["review_title"] = safe_text(block.find("h2", class_="text_header"))

            # review text + trip verified
            text_div = block.find("div", class_="text_content", itemprop="reviewBody")
            if text_div:
                text = text_div.get_text(" ", strip=True)
                record["review_text"] = text
                record["trip_verified_flag"] = "trip verified" in text.lower()

            # ratings table
            rows = block.select("table.review-ratings tr")

            for row in rows:
                header = row.find("td", class_="review-rating-header")
                value = row.find("td", class_="review-value")
                stars = row.find("td", class_="review-rating-stars")

                if not header:
                    continue

                label = header.get_text(strip=True).lower()

                # simple text fields
                if value:
                    val = value.get_text(strip=True)

                    if "aircraft" in label:
                        record["aircraft_model"] = val
                    elif "type of traveller" in label:
                        record["traveller_type"] = val.lower()
                    elif "seat type" in label:
                        record["seat_class"] = val.lower()
                    elif "route" in label and " to " in val.lower():
                        o, d = val.split(" to ", 1)
                        record["route_origin"] = o.strip()
                        record["route_destination"] = d.strip()
                    elif "date flown" in label:
                        record["flight_date"] = val
                    elif "recommended" in label:
                        record["recommended_flag"] = val.lower() == "yes"

                # star ratings
                if stars:
                    rating = len(stars.select("span.star.fill"))

                    if "seat comfort" in label:
                        record["seat_comfort_rating"] = rating
                    elif "cabin staff" in label:
                        record["cabin_staff_rating"] = rating
                    elif "food" in label:
                        record["food_beverage_rating"] = rating
                    elif "ground service" in label:
                        record["ground_service_rating"] = rating
                    elif "value for money" in label:
                        record["value_for_money_rating"] = rating

            reviews.append(record)

        except Exception as e:
            print(f"Skipping review due to parse error: {e}")

    return reviews


def get_data(base_url: str, pages: int, page_size: int) -> List[Dict]:
    all_reviews = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(fetch_page_reviews, base_url, page, page_size)
            for page in range(1, pages + 1)
        ]

        for future in concurrent.futures.as_completed(futures):
            all_reviews.extend(future.result())

    print(f"Scraping completed: {len(all_reviews)} reviews collected.")
    return all_reviews


def save_data_csv(data: List[Dict], file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Saved {len(df)} rows → {file_path}")


# Define base URL and scraping parameters
base_url = "https://www.airlinequality.com/airline-reviews/united-airlines"
pages = PAGES
page_size = PAGE_SIZE

reviews = get_data(base_url, pages, page_size)

csv_file_path = "./Data/reviews.csv"
if reviews:
    save_data_csv(reviews, csv_file_path)
else:
    print("Unable to collect reviews")
