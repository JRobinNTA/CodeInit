import scrapy
import json
import logging
from scrapy.utils.log import configure_logging
from scrapy.exceptions import CloseSpider
import os
from bs4 import BeautifulSoup
import re

class InterviewDiariesSpider(scrapy.Spider):
    name = 'interview_diaries'
    allowed_domains = ['sites.google.com']
    start_urls = ['https://sites.google.com/nitc.ac.in/interviewdiaries/']

    # Words to filter out
    filter_words = [
        "Search this site",
        "Embedded Files",
        "Skip to main content",
        "Skip to navigation",
        "Interview Diaries",
        "GE healthcare",
        "2023 | ISSUE | ARTICLE",
        "Report abuse"
        "check out the ARCHIVES for more"
        "ABOUT"
        "Interview diaries"
        "2023 ARTICLES ARE UPDATED"
    ]

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='spider_log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def __init__(self, *args, **kwargs):
        super(InterviewDiariesSpider, self).__init__(*args, **kwargs)
        cookie_path = '/home/johnr/Documents/Devel/Contain/Scrape/codinitscrape/cookies.json'
        self.logger.info(f"Loading cookies from: {cookie_path}")
        self.cookies = self.load_cookies(cookie_path)
        # Create/clear the output text file
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write('')

    def load_cookies(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                cookies_data = json.load(f)
                cookies_dict = {}
                for cookie in cookies_data:
                    name = cookie.get('Name raw')
                    content = cookie.get('Content raw')
                    if name and content:
                        cookies_dict[name] = content
                self.logger.info(f"Total cookies loaded: {len(cookies_dict)}")
                return cookies_dict
        except Exception as e:
            self.logger.error(f"Error loading cookies: {str(e)}")
            return {}

    def start_requests(self):
        if not self.cookies:
            self.logger.error("No cookies loaded! Stopping spider.")
            raise CloseSpider('No cookies available')

        self.logger.info(f"Starting request to: {self.start_urls[0]}")

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                cookies=self.cookies,
                callback=self.parse,
                errback=self.errback_httpbin,
                dont_filter=True,
                meta={'dont_merge_cookies': False}
            )

    def extract_content(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        # Remove script and style elements
        for element in soup.find_all(['script', 'style']):
            element.decompose()

        all_text = []

        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']):
            text = tag.get_text(strip=True)
            if text and not text.isspace():
                # Filter out unwanted text
                if text not in self.filter_words and not any(word in text for word in self.filter_words):
                    all_text.append(text)

        return all_text

    def parse(self, response):
        self.logger.info(f"Parsing response from: {response.url}")
        self.logger.info(f"Response status: {response.status}")

        if self.check_authentication(response):
            self.logger.info("Successfully authenticated!")

            content = []
            elements = response.xpath('//*[self::p or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6 or self::span or self::div]/text()').getall()

            # Clean and filter the extracted text
            for element in elements:
                text = element.strip()
                if text and not text.isspace():
                    if text not in self.filter_words and not any(word in text for word in self.filter_words):
                        content.append(text)

            # If no content found with xpath, try using BeautifulSoup
            if not content:
                content = self.extract_content(response)

            # Write clean content to file
            if content:
                with open('output.txt', 'a', encoding='utf-8') as f:
                    for text in content:
                        f.write(text + '\n')

            # Follow links
            links = response.xpath('//a/@href').getall()
            for link in links:
                if link and isinstance(link, str) and link.startswith('/nitc.ac.in/interviewdiaries/'):
                    full_url = f'https://sites.google.com{link}'
                    self.logger.info(f"Following link: {full_url}")
                    yield scrapy.Request(
                        url=full_url,
                        cookies=self.cookies,
                        callback=self.parse,
                        errback=self.errback_httpbin
                    )
        else:
            self.logger.error("Authentication failed!")
            self.logger.error(f"Response preview: {response.text[:500]}")
            raise CloseSpider('Authentication failed')

    def check_authentication(self, response):
        if response.status == 200:
            return True
        return False

    def errback_httpbin(self, failure):
        self.logger.error(f"Request failed: {failure.value}")
