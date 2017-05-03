from requests import get
from bs4 import BeautifulSoup
from collections import OrderedDict as OD

# Reduce clutter
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

BASE_URL = "http://www.broadcastify.com/listen/"


def cook_soup(path):
    return BeautifulSoup(get(BASE_URL+path).text)


def get_ids(path, name, skip=False):
    """Scrapes stids, ctids and mids from boxes and dropdowns."""
    soup = cook_soup(path)
    select = soup.find("select", {"name": name})
    if not select:
        raise Exception("Can't find box for {}".format(name))
    ids = OD()
    for i in select.find_all("option"):
        ids[i.text] = i["value"][5 if skip else 0:]
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
        if not cells:
            continue
        desc = cells[1].find("span", "rrfont")
        feed = OD([
            ("name", cells[1].find("a").text),
            ("desc", desc.text.strip() if desc else None),
            ("id", cells[1].find("a")["href"][13:]),
            ("genre", cells[2].text.strip()),
            ("listeners", int(cells[3].text)),
            ("status", cells[-1].text)
        ])
        feeds.append(feed)
    return feeds


def get_stream_url(id):
    audio = cook_soup("feed/{}/web".format(id)).find("audio")
    return audio["src"] if audio else None


def get_ctid_from_zip(zip):
    return get(BASE_URL, allow_redirects=False,
               params={"action": "searchZip",
                       "zip": zip}).headers["location"].split("/")[-1]
