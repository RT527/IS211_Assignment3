#Rafi Talukder Assignment_3
import argparse
import urllib.request
import io
from datetime import datetime


def download_data(url: str) -> str: #Download data from a URL and return it as decoded text.
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")

def dict_data(data: str): #CSV text -> list of dictionaries
    records = []
    reader = csv.reader(io.StringIO(data))
    for row in reader:
        if len(row) != 5:
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


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

