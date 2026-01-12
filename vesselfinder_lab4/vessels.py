from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time
import sys

sys.stdout.reconfigure(line_buffering=True)

def create_http_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8',
        'Connection': 'keep-alive',
    })
    return session


def fetch_page(session, url, timeout=60):
    response = session.get(url, timeout=timeout)
    if response.status_code != 200:
        return None, response.status_code
    return BeautifulSoup(response.text, "html.parser"), None

def parse_search_page(search_soup, vessel_data):
    if search_soup.find("div", {"class": "no-result-row"}):
        print("No search results found")
        return True
    pagination_block = search_soup.find("div", {"class": "pagination-totals"})
    if not pagination_block:
        print("Pagination block not found")
        return False
    vessels_found = int(re.search(r"(\d+)", pagination_block.text).group(1))
    if vessels_found != 1:
        print(f"Multiple vessels found: {vessels_found}. Skipping")
        return True

    vessel_name = search_soup.find("div", {"class": "slna"}).text
    vessel_type = search_soup.find("div", {"class": "slty"}).text
    ship_link = search_soup.find("a", {"class": "ship-link"})
    imo_match = re.search(r"/details/(\d+)", ship_link.get("href"))
    imo_number = imo_match.group(1)
    vessel_data["Name"].append(vessel_name)
    vessel_data["IMO"].append(imo_number)
    vessel_data["Type"].append(vessel_type)
    print(f"Vessel found: {vessel_name}, IMO {imo_number}")

    return imo_number

def parse_details_page(details_soup, vessel_data):
    for script in details_soup.find_all("script"):
        if not script.string:
            continue
        mmsi_match = re.search(r"var MMSI=(\d+)", script.string)
        if mmsi_match:
            vessel_data["MMSI"].append(mmsi_match.group(1))
            print(f"MMSI extracted: {mmsi_match.group(1)}")
            return True
    print("MMSI not found on details page")
    return False

def process_search_url(session, url, vessel_data, failed_urls):
    print(f"Processing URL: {url}")
    search_soup, error_code = fetch_page(session, url)
    if not search_soup:
        print(f"Search page load failed. HTTP status: {error_code}")
        failed_urls.append((url, error_code))
        return False
    result = parse_search_page(search_soup, vessel_data)

    if result is True:
        print("Search page processed\n")
        return True
    if not result:
        print("Search page processing failed\n")
        return False

    details_url = f"https://www.vesselfinder.com/ru/vessels/details/{result}"
    print("Loading vessel details page...")

    details_soup, error_code = fetch_page(session, details_url)
    if not details_soup:
        print(f"Details page load failed. HTTP status: {error_code}")
        failed_urls.append((details_url, error_code))
        return False
    success = parse_details_page(details_soup, vessel_data)
    print("Details page processed...\n")
    return success

def main():
    vessel_data = {
        "Name": [],
        "IMO": [],
        "MMSI": [],
        "Type": []
    }

    failed_urls = []
    success_pages = 0
    session = create_http_session()
    session.get("https://www.vesselfinder.com/", timeout=10)
    time.sleep(2)
    input_links = pd.read_excel("Links.xlsx")
    total_links = len(input_links)

    for index, url in enumerate(input_links["Ссылка"], start=1):
        print(f"[{index}/{total_links}]")
        if process_search_url(session, url, vessel_data, failed_urls):
            success_pages += 1
    result_dataframe = pd.DataFrame(
        vessel_data,
        columns=["Name", "IMO", "MMSI", "Type"]
    )
    result_dataframe.to_excel("OutputLinks.xlsx", index=False)

    print("Processing finished")
    print(f"Successful pages: {success_pages}")
    print(f"Failed pages: {len(failed_urls)}")
    print(failed_urls)

if __name__ == "__main__":
    main()
