import concurrent.futures
from bs4 import BeautifulSoup
import requests
import multiprocessing
import random
import os
import re

def download(url, dir_name="files"):
    output = []
    title = "".join(i for i in url if i.isalpha())
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find(id="bodyContent").find_all("a")
    links = [f"http://wikipedia.org/{link.get('href')}" for link in data]
    links = random.choices(links, k=10)
    if not os.path.isdir(f"{dir_name}"):
        os.mkdir(f"{dir_name}")
    with open(f"files/{title}.txt", "w") as f:
        for i in links:
            if re.match(r"^http://wikipedia\.org//wiki/[\w0-9]+$", i):
                output.append(i)
                f.write(i+"\n"+"\n")
    return output


def extract_citations(url):
    citations = []
    response = requests.get(url)
    bs = BeautifulSoup(response.content, features="html.parser")
    title = bs.find(id="firstHeading").text
    bs = [i.text for i in bs.find_all("span", "reference-text")]
    print(bs)
    bs = [str(i).split("^") for i in bs]
    print(bs)
    for i in bs:
        for j in i:
            if len(j) > 1: citations.append(j)

    if not os.path.isdir("references"): os.mkdir("references")
    with open(f"references/{title}.txt", "w", encoding='utf-8') as fh:
        for i in sorted(citations):
            if len(i) > 1: fh.write(i+"\n\n")

def pool(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, urls)

def main(url, count, crawl_depth):
    links = download(url)
    if count > crawl_depth:
        return
    for i in links:
        p = multiprocessing.Process(target=main, args=(i, count + 1, crawl_depth))
        p.start()
    pool(links)


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Brain"
    """
    main(url, 0, 2)
    """
    #extract_citations(url)
