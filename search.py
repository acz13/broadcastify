import requests
from bs4 import BeautifulSoup

# Reduce clutter
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

BASE_URL = "http://www.broadcastify.com/listen/"


def cook_soup(path):
    return BeautifulSoup(requests.get(BASE_URL+path).text)


def get_ids(path, name, skip=False):
    """Scrapes stids, ctids and mids from boxes and dropdowns."""
    soup = cook_soup(path)
    select = soup.find("select", {"name": name})
    if not select:
        raise Exception("Can't find box for {}".format(name))
    ids = {}
    for i in select.children:
        ids[i.text] = i["value"][4 if skip else 0:]
    return ids


def get_feeds(path):
    soup = cook_soup(path)
    feeds = []
    try:
        rows = soup.select("table.btable tr")[1:]  # No <tbody>
    except TypeError:
        return []
    for row in rows:
        cells = row.find_all("td")
        desc = cells[1].find("span", "rrfont")
        feed = {
            "name": cells[1].find("a").text,
            "desc": desc.text.strip() if desc else None,
            "id": cells[1].find("a")["href"][13:],
            "genre": cells[2].text.strip(),
            "listeners": int(cells[3].text),
            "status": cells[-1].text
        }
        feeds.append(feed)
    return feeds


def get_stream_url(id):
    audio = cook_soup("feed/{}/web".format(id)).find("audio")
    return audio["src"] if audio else None
