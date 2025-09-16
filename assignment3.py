#Rafi Talukder Assignment_3
import argparse
import urllib.request

def download_data(url: str) -> str: #Download data from a URL and return it as decoded text.
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")

def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

