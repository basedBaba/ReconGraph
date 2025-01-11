#! /usr/bin/env python3
"""
Sagemode: Track and Unveil Online identities across social media platforms.
"""
import os
import re
import datetime
import subprocess
import threading
import random
import requests
import json
from argparse import ArgumentParser

from bs4 import BeautifulSoup

from sites import sites, soft404_indicators, user_agents


class Sagemode:
    def __init__(self, username: str, found_only=False):
        #self.console = Console()
        self.positive_count = 0
        self.username = username
        self.result_file = os.path.join(f"{self.username}.json")
        self.found_only = found_only
        self.results = {"found": [], "not_found": []}

    def is_soft404(self, html_response: str) -> bool:
        soup = BeautifulSoup(html_response, "html.parser")
        page_title = soup.title.string.strip() if soup.title else ""

        for error_indicator in soft404_indicators:
            if (
                error_indicator.lower() in html_response.lower()
                or error_indicator.lower() in page_title.lower()
                or page_title.lower() == "instagram"
                or page_title.lower() == "patreon logo"
                or "sign in" in page_title.lower()
            ):
                return True
        return False

    def check_site(self, site: str, url: str, headers):
        url = url.format(self.username)
        try:
            with requests.Session() as session:
                response = session.get(url, headers=headers)

            if (
                response.status_code == 200
                and self.username.lower() in response.text.lower()
                and not self.is_soft404(response.text)
            ):
                with threading.Lock():
                    self.positive_count += 1
                self.results["found"].append({"site": site, "url": url})
            else:
                if not self.found_only:
                    self.results["not_found"].append({"site": site})
        except Exception as e:
            print(f"Error checking {site}: {e}")
            #raise Exception(e)


    def start(self):
        #self.console.print(f"Starting search for username: {self.username}")

        current_datetime = datetime.datetime.now()
        date = current_datetime.strftime("%m/%d/%Y")
        time = current_datetime.strftime("%I:%M %p")
        headers = {"User-Agent": random.choice(user_agents)}

        # with open(self.result_file, "a") as file:
        #     file.write(json.dumps({"date": date, "time": time, "results": []}, indent=4))

        threads = []

        try:
            for site, url in sites.items():
                thread = threading.Thread(target=self.check_site, args=(site, url, headers))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

            # with open(self.result_file, "w") as f:
            #     json.dump(self.results, f, indent=4)

            # print(f"Search complete. Results saved to {self.result_file}")

        except Exception:
            raise Exception(e)

        return self.results["found"]


def sagemode_wrapper(username: str):
    """
    Wrapper function to use Sagemode as a package.

    Args:
        username (str): The username to search for.

    Returns:
        dict: JSON-compatible dictionary containing the results of the search.
    """
    sage = Sagemode(username)
    results = sage.start()
    return results


def main():

    print(sagemode_wrapper("0xRavenspar"))



if __name__ == "__main__":
    main()
