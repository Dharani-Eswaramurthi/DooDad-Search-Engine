from bs4 import BeautifulSoup
from urllib.parse import urlparse
from settings import *

with open("blacklist.txt") as f:
    domains=set(f.read().split("\n"))

def get_page_content(row):
    soup=BeautifulSoup(row["html"], features="html.parser")
    text = soup.get_text()
    return text

def tracker_urls(row):
    soup= BeautifulSoup(row["html"])
    scripts = soup.find_all("script", {"src": True})
    srcs = [s.get("src") for s in scripts]

    links=soup.find_all("a", {"href": True})
    href=[l.get("href") for l in links]
    all_domains = [urlparse(s).hostname for s in srcs + href]
    return len(all_domains)

class Filter():
    def __init__(self, results) -> None:
        self.filtered=results.copy()

    def content_filter(self):
        page_content = self.filtered.apply(get_page_content, axis=1)
        word_count = page_content.apply(lambda x: len(x.split(" ")))
        word_count/=word_count.mode()
        self.filtered["rank"] += word_count

    def tracker_filter(self):
        tracker_count=self.filtered.aplly(tracker_urls, axis=1)
        self.filtered["rank"] += tracker_count

    def filter(self):
        self.content_filter()
        self.filtered = self.filtered.sort_values("rank", ascending=True)
        self.filtered["rank"] = self.filtered["rank"].round()
        return self.filtered