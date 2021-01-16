from bs4 import BeautifulSoup, SoupStrainer
import requests
import string
import pprint


class Crawler:
    def __init__(self, root, branches=[], parent_child_dict=None):
        self.root = root
        self.branches = branches
        self.parent_child_dict = parent_child_dict
        self.text = None

    def scrape(self):
        data = requests.get(self.root)
        bs = BeautifulSoup\
            (data.content,
             parse_only=SoupStrainer("a"),
             features="html.parser")

        for i in bs:
            if i.has_attr("href"):
                self.branches.append(i.get("href"))
        return self.branches

    def construction(self):
        if not self.branches:
            return
        else:
            self.parent_child_dict \
                = {
                self.root: [f"{self.root[:-1]}{i}"
                for i in self.branches
                    if i != "/"]
            }
        return self.parent_child_dict

    def pretty_print(self):
        if not self.parent_child_dict:
            return
        for k, v in self.parent_child_dict.items():
            print("ROOT:")
            print(f"{k}\n")
            print("VALUES:")
            for i in v:
                print(f"{i}")

    def extract_txt(self):
        data = requests.get(self.root)
        soup = BeautifulSoup(data.content, features="html.parser")
        soup = str(soup.text)
        trans = soup.maketrans("", "", string.punctuation)
        soup = soup.translate(trans)
        soup = soup.replace("\n", " ").replace("\r", " "). \
            replace(":", "").replace(";", "").split(" ")
        soup = [i.strip().lower() for i in soup if i.isalpha()]
        self.text = {self.root: soup}


spider1=Crawler("https://www.britannica.com/")
print(spider1.extract_txt())
pprint.pprint(spider1.text)

