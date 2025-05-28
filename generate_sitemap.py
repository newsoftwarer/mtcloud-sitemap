import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

BASE_URL = "https://www.mtclouds.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}
visited = set()
urls = []

def crawl(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200 or "text/html" not in res.headers.get("Content-Type", ""):
            return
        visited.add(url)
        soup = BeautifulSoup(res.text, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(url, href)
            if full_url.startswith(BASE_URL):
                clean_url = full_url.split("#")[0].rstrip("/")
                if clean_url not in visited and clean_url not in urls:
                    urls.append(clean_url)
                    crawl(clean_url)
    except Exception as e:
        print(f"Error crawling {url}: {e}")

def write_sitemap_xml():
    today = datetime.today().strftime("%Y-%m-%d")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in sorted(urls):
            f.write(f"  <url><loc>{url}</loc><lastmod>{today}</lastmod></url>\n")
        f.write("</urlset>\n")

def write_sitemap_html():
    with open("sitemap.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html lang='zh-Hant'>\n<head><meta charset='UTF-8'>\n")
        f.write("<title>網站地圖</title>\n<style>body{font-family:sans-serif;padding:2em;max-width:800px;margin:auto;background:#f9f9f9;}ul{list-style:none;padding-left:1em;}li{margin-bottom:.3em;}a{color:#06c;text-decoration:none;}a:hover{text-decoration:underline;}</style></head><body>\n")
        f.write("<h1>網站地圖</h1>\n<ul>\n")
        for url in sorted(urls):
            f.write(f"<li><a href='{url}'>{url}</a></li>\n")
        f.write("</ul>\n</body>\n</html>\n")

if __name__ == "__main__":
    crawl(BASE_URL)
    write_sitemap_xml()
    write_sitemap_html()
