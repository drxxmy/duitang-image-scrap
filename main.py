import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_headers import Headers
import time
import os


class DuitangParser:
    def __init__(
        self, keyword: str, scroll_number: int = 10, sleep_timer: int = 1
    ) -> None:
        """
        Parameters
        ----------
        keyword : str
            Duitang search keyword.
        scroll_number : int
            Number of scrolls to load the page.
        sleep_timer : int
            Sleep time after executing a web request.
        """
        self.keyword = keyword
        self.scroll_number = scroll_number
        self.sleep_timer = sleep_timer
        self.url = f"http://www.duitang.com/search/?kw={keyword}&type=feed"

    def get_html_data(self, url: str, headers: dict = None) -> str:
        """This method is used to get html data from a web page.

        Headers are used to bypass the spam detection system in some cases.

        Parameters
        ----------
        url : str
            Link to the page to retrieve HTML data.
        headers : dict
            Headers for a web request.
        """
        while 1:
            try:
                response = requests.get(url=url, headers=headers)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as e:
                print("HTTPError({0}): {1}".format(e.errno, e.strerror), e)
                exit(1)
            except requests.exceptions.ConnectionError as e:
                time.sleep(5)
            except requests.exceptions.Timeout as e:
                print("Timeout({0}): {1}".format(e.errno, e.strerror), e)
                exit(1)
            except requests.exceptions.RequestException as e:
                print("OOps({0}): {1}".format(e.errno, e.strerror), e)
                exit(1)
        return response.text

    def get_image_source(self, html_data: str) -> str:
        """This method is used to get the image source from the html code.

        Parameters
        ----------
        html_data : str
            HTML data of the page with an image.
        """
        soup = BeautifulSoup(html_data, "html.parser")
        image_src = soup.find("img", {"id": "mbpho-img"})
        if image_src != None:
            return image_src["src"]
        else:
            print("Couldn't get image source for one page.")

    def run(self):
        """This method is used to run a process of web scraping and downloading images."""
        print(f"Running a script for '{self.url}', keyword is '{self.keyword}'")
        headers = Headers()
        blog_urls = self.get_blog_urls()
        if blog_urls:
            print(
                f"Successfully obtained links to individual image pages - {len(blog_urls)} links!"
            )
        else:
            print("Failed to get any links to individual image pages.")
            exit(1)
        image_urls = []

        for blog_url in blog_urls:
            header = headers.generate()
            html_data = self.get_html_data(url=blog_url, headers=header)
            image_source = self.get_image_source(html_data)
            image_urls.append(image_source)
            print(
                f"({len(image_urls)}/{len(blog_urls)}) | Getting the source image from the page!"
            )
        print("Successfully obtained image sources from the pages!")

        os.makedirs("images", exist_ok=True)
        os.chdir("images")
        os.makedirs(self.keyword, exist_ok=True)
        os.chdir(self.keyword)

        file_counter = 0
        for url in image_urls:
            self.download_image(url)
            file_counter += 1
            print(f"({file_counter}/{len(image_urls)}) | Saved file to {os.getcwd()}\ ")
        print("Script finished working!")

    def download_image(self, image_url: str) -> None:
        """This method is used to download images from a specified url.

        Parameters
        ----------
        image_url : str
            Image link.
        """
        try:
            image_data = requests.get(image_url).content
        except requests.exceptions.HTTPError as e:
            print("HTTPError({0}): {1}".format(e.errno, e.strerror), e)
            exit(1)
        except requests.exceptions.ConnectionError as e:
            time.sleep(5)
        except requests.exceptions.Timeout as e:
            print("Timeout({0}): {1}".format(e.errno, e.strerror), e)
            exit(1)
        except requests.exceptions.RequestException as e:
            print("OOps({0}): {1}".format(e.errno, e.strerror), e)
            exit(1)
        filename = image_url.split("/")[
            -1
        ]  # -- The last part of the link is used as a filename.
        try:
            with open(filename, "wb") as handler:
                handler.write(image_data)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror), e)
            print("Skipped this file.")

    def get_blog_urls(self) -> list:
        """This method is used to get blog urls from a web page."""
        blog_urls = []

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)
        print("Browser window is open.")
        driver.get(self.url)

        for _ in range(self.scroll_number):
            driver.execute_script("window.scrollTo(1,100000)")
            print(f"Performed scrolling {_+1} time(s).")
            time.sleep(self.sleep_timer)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        for found_item in soup.find_all("a", {"class": "a"}):
            blog_urls.append(f"http://www.duitang.com{(found_item.attrs['href'])}")

        return blog_urls
