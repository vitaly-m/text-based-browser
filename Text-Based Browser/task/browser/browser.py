import argparse
import os
import collections
import requests
from bs4 import BeautifulSoup
import colorama

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory where to save oen pages")

args = parser.parse_args()
if not os.path.exists(args.dir):
    os.mkdir(args.dir)


def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="html.parser")
    elements = soup.find_all(("p", "a", "ul", "ol", "li"))
    return "\n".join(colorama.Fore.BLUE + e.get_text() if e.name == "a" else colorama.Fore.RESET + e.get_text() for e in elements)


# write your code here
history = collections.deque()
colorama.init()
while True:
    site = input()
    if site == "exit":
        break
    elif site == "back":
        if len(history) > 1:
            history.pop()
            print(history.pop())
        continue
    file_name = f"{args.dir}/{site}"
    if os.path.exists(file_name):
        content = ""
        with open(file_name, "r") as file:
            for line in file:
                content += line.strip()
        print(content)
        history.append(content)
    elif not site.__contains__("."):
        print("Error: Incorrect URL")
    else:
        body = get_content("https://" + site)
        print(body)
        history.append(body)
        with open(f"{args.dir}/{site[:site.rfind('.')]}", "w") as file:
            file.write(body)
colorama.deinit()
