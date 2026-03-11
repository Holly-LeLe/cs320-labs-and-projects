'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 3 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP4
Student 1: zhengyang yu, zyu447
Student 2: Holly Li, wli682
Student 3: renxiang chao, rchao5
'''

# Add additional imports if needed

import os
from collections import deque
from io import StringIO
import time
import requests
import pandas as pd
from selenium.webdriver.common.by import By
from urllib.parse import urljoin



class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ 
        Leave this method as is! It will be over-written the child classes
        Each child class should perform the following:
            Record the node value in self.order AND return its children
            parameter: node
            return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set and order list
        # 2. start recursive search by calling dfs_visit
        # 1) reset
        self.visited = set()
        self.order = []
        # 2) run recursion
        self.dfs_visit(node)

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        # 2. mark node as visited by adding it to the set
        # 3. call self.visit_and_get_children(node) to get the children
        # 4. in a loop, call dfs_visit on each of the children
        if node in self.visited:
            return
        self.visited.add(node)
        children = self.visit_and_get_children(node)
        for child in children:
            self.dfs_visit(child)

    def bfs_search(self, node):
        # TODO: implement bfs
        # reset
        self.visited = set()
        self.order = []

        q = deque()
        q.append(node)
        self.visited.add(node)

        while q:
            cur = q.popleft()
            children = self.visit_and_get_children(cur)
            for child in children:
                if child not in self.visited:
                    self.visited.add(child)
                    q.append(child)


class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)

        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        row = self.df.loc[node]
        for col, val in row.items():
            if int(val) == 1:
                children.append(col)
        return children


class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()

    def visit_and_get_children(self, node):
        path = os.path.join("file_nodes", node)
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]

        value = lines[0].strip() if len(lines) > 0 else ""
        self.order.append(value)

        if len(lines) < 2 or lines[1].strip() == "":
            return []

        children = [x.strip() for x in lines[1].split(",") if x.strip() != ""]
        return children

    def concat_order(self):
        return "".join(self.order)


class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tables = []

    def visit_and_get_children(self, node):
        # record node in visit order
        self.order.append(node)

        # visit page
        self.driver.get(node)

        # read tables; keep ONLY the travellog fragment table
        try:
            dfs = pd.read_html(node)
            want = {"clue", "latitude", "longitude", "description"}

            for t in dfs:
                # normalize column names for matching
                cols = [str(c).strip().lower() for c in t.columns]
                if want.issubset(set(cols)):
                    t2 = t.copy()
                    t2.columns = cols  # force exact column names like the csv
                    # keep only the 4 columns, in a stable order
                    t2 = t2[["clue", "latitude", "longitude", "description"]]
                    self.tables.append(t2)
                    break  # only one per page
        except ValueError:
            pass

        # collect links
        links = []
        a_tags = self.driver.find_elements(By.TAG_NAME, "a")
        for a in a_tags:
            href = a.get_attribute("href")
            if href:
                links.append(href)

        # dedupe, preserve order
        seen = set()
        out = []
        for x in links:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def table(self):
        if not self.tables:
            return pd.DataFrame(columns=["clue", "latitude", "longitude", "description"])
        return pd.concat(self.tables, ignore_index=True)


def get_password(travellog):
    """
    Given a DataFrame-like object with a 'clue' column,
    combine values into a password string.
    """
    # travellog is a DataFrame with column 'clue'
    parts = []
    for x in travellog["clue"].tolist():
        parts.append(str(x))
    return "".join(parts)
def reveal_secrets(driver, url, travellog):
    password = get_password(travellog)

    driver.get(url)

    password_box = driver.find_element(By.TAG_NAME, "input")
    password_box.clear()
    password_box.send_keys(password)

    go_button = driver.find_element(By.TAG_NAME, "button")
    go_button.click()
    time.sleep(2)

    buttons = driver.find_elements(By.TAG_NAME, "button")
    view_button = buttons[0]
    for b in buttons:
        if "View" in b.text:
            view_button = b
            break
    view_button.click()
    time.sleep(2)

    location = driver.find_element(By.TAG_NAME, "h4").text

    img = driver.find_element(By.TAG_NAME, "img")
    img_url = img.get_attribute("src")

    r = requests.get(img_url)
    r.raise_for_status()

    with open("Current_Location.jpg", "wb") as f:
        f.write(r.content)

    return location