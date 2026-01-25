'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 3 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP4
Student 1: <Name>, <NETID>
Student 2: <Name>, <NETID>
Student 3: <Name>, <NETID>
'''

# Add additional imports if needed

from collections import deque
from io import StringIO
import time
import requests
import pandas as pd
from selenium.webdriver.common.by import By


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

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        # 2. mark node as visited by adding it to the set
        # 3. call self.visit_and_get_children(node) to get the children
        # 4. in a loop, call dfs_visit on each of the children

    def bfs_search(self, node):
        # TODO: implement bfs
        pass


class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__()
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        return children


class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()

    def visit_and_get_children(self, node):
        # TODO: open the file in file_nodes, then parse the value and children
        # TODO: record value in self.order
        pass

    def concat_order(self):
        # TODO: return joined string of self.order
        pass


class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tables = []

    def visit_and_get_children(self, node):
        # TODO: record node in self.order
        # TODO: fetch the page, parse HTML table into pandas, store it
        # TODO: return list of links (<a> tags)
        pass

    def table(self):
        # TODO: return combined DataFrame
        pass


def get_password(travellog):
    """
    Given a DataFrame-like object with a 'clue' column,
    combine values into a password string.
    """
    # TODO: build string from travellog['clue']
    pass


def reveal_secrets(driver, url, travellog):
    """
    Automate secret-revealing:
    1. Generate clue/password
    2. Enter password into webpage
    3. Click buttons, wait for image
    4. Save image
    5. Return the location text
    """
    # TODO: implement using Selenium driver, retries, and requests
    pass