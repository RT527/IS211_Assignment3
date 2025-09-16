#Rafi Talukder Assignment_3
import argparse
import csv
import urllib.request
import re
import io
from datetime import datetime
"""---------------------------------------------------------------------------------"""
def download_data(url: str) -> str: #Download data from a URL and return it as decoded text.
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")
"""---------------------------------------------------------------------------------"""
def dict_data(data: str): #CSV text -> list of dictionaries
    records = []
    reader = csv.reader(io.StringIO(data))
    for row in reader:
        if len(row) != 5: # This will help skip the bad rows
            continue

        path, dt_str, browser, status, size = row
        try:
            timestamp = datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S")
        except ValueError: # This will skip the rows with bad date times
            continue

        records.append({
            "path": path,
            "datetime": timestamp,
            "browser": browser,
            "status": status,
            "size": size
        })
    return records
"""---------------------------------------------------------------------------------"""
def img_stats(records): # Uses regex to find and count images and give percent
    img_regex = re.compile(r".*\.(gif|png|jpg)$", re.IGNORECASE)
    total = len(records)
    img_hits = sum(1 for r in records if img_regex.match(r["path"]))
    percent = (img_hits/total * 100) if total > 0 else 0
    print(f"The image requests account for {percent:.1f}% of all requests =)")
"""---------------------------------------------------------------------------------"""
def main(url: str):
    print(f"Running main with URL = {url}...")

    try:
        raw_data = download_data(url)
    except Exception as e:
        print(f"Sorry =(. Error downloading the file: {e}")
        return

    records = dict_data(raw_data)
    if not records:
        print("Oh oh, there is no data to process. Check file format please.")
        return
    #assignment functions
    img_stats(records)
"""---------------------------------------------------------------------------------"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Week 3 Assignment")
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

