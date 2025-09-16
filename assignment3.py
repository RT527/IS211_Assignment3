#Rafi Talukder Assignment_3
import argparse
import csv
import urllib.request
import re
from datetime import datetime
from collections import defaultdict
"""---------------------------------------------------------------------------------"""
def download_data(url): # Download data from a URL and return it as decoded text.
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')
"""---------------------------------------------------------------------------------"""
def dict_data(data): # CSV text -> list of dictionaries
    reader = csv.reader(data.splitlines())
    return list(reader)
"""---------------------------------------------------------------------------------"""
def img_stats(records):  # Uses regex to find and count images and give percent
    img_hits = 0
    img_regex = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)
    for row in records:
        if row and img_regex.search(row[0]):
            img_hits += 1

    total_hits = len(records)
    percentage = (img_hits / total_hits) * 100 if total_hits > 0 else 0
    return {
        'total': total_hits,
        'images': img_hits,
        'percentage': percentage
    }
"""---------------------------------------------------------------------------------"""
def best_browser(records): # This will use regext to check user agent string and find most used browser
    b_count = defaultdict(int)
    b_pats = {
        'Firefox': re.compile(r'Firefox'),
        'Chrome': re.compile(r'Chrome'),
        'Internet Explorer': re.compile(r'MSIE|Trident'),
        'Safari': re.compile(r'Safari(?!.*Chrome)')
    }
    for row in records:
        if not row or len(row) < 3:
            continue

        user_agent = row[2]
        for browser, pattern in b_pats.items():
            if pattern.search(user_agent):
                b_count[browser] += 1
                break

    if not b_count:
        return None

    most_popular = max(b_count.items(), key=lambda x: x[1])
    return {
        'counts': b_count,
        'most_popular': most_popular
    }
"""---------------------------------------------------------------------------------"""
def hourly_hits(records): #extra credit to count requests per hour and sort hit count
    hour_counts = defaultdict(int)
    for row in records:
        if not row or len(row) < 2:
            continue

        try:
            dt = datetime.strptime(row[1].strip(), '%m/%d/%Y %H:%M:%S')
            hour_counts[dt.hour] += 1
        except ValueError:
            continue

    for hour in range(24):
        if hour not in hour_counts:
            hour_counts[hour] = 0

    return sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
"""---------------------------------------------------------------------------------"""
def main():
    print(f"Downloading log data from {args.url}")
    csv_data = download_data(args.url)
    log_data = dict_data(csv_data)

    image_stats = img_stats(log_data)
    print(f"\nImage requests account for {image_stats['percentage']:.1f}% of all requests")

    browser_stats = best_browser(log_data)
    if browser_stats:
        browser, count = browser_stats['most_popular']
        print(f"\nMost popular browser is {browser} with {count} hits")

    #extra credit
    hour_stats = hourly_hits(log_data)
    print("\nHourly traffic statistics (sorted by hits):")
    for hour, count in hour_stats:
        print(f"Hour {hour:02d} has {count} hits")
"""---------------------------------------------------------------------------------"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Week 3 Assignment")
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main()
