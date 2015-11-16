import re

import requests
from bs4 import BeautifulSoup

from appium_selector.CapGenerators.GridMobile import GridMobile
from appium_selector.CapGenerators.GridMobileWeb import GridMobileWeb
from appium_selector.CapGenerators.GridWeb import GridWeb
from appium_selector.Helpers.Config import GetConfig


class GridConnector(object):

    webNodes = []
    mobileNodes = []
    browsers = ['chrome', 'firefox', 'ie', 'safari', 'edge']

    def __init__(self):
        for node in self._getNodes():
            self._parseNodes(node)

    def _getNodes(self):
        try:
            page = requests.get(GetConfig('GRID_URL') + '/grid/console')
            soup = BeautifulSoup(page.text, 'html.parser')
            resultsWeb = soup.select('img[title*=WebDriver]')
            resultsMobile = soup.select('a[title*=platform]')
            return resultsWeb + resultsMobile
        except:
            return []

    def _parseNodes(self, node):
        if 'deviceName' not in node['title']:
            self.webNodes.append(GridWeb(node['title']))
        elif self._propertyFromTitle('browserName', node['title']) in self.browsers:
            self.webNodes.append(GridMobileWeb(node['title']))
        else:
            self.mobileNodes.append(GridMobile(node['title']))

    def _propertyFromTitle(self, property, title):
        return re.search(property + '=.*?[}|,]', title).group().split('=')[1].replace('}','').replace(',','')

