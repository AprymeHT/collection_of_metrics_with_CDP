"""
headless mode
"""

import time
import pychrome
import json
import json2html.jsonconv
import base64
import os
import glob


class EventHandler(object):
    def __init__(self, browser, tab):
        self.browser = browser
        self.tab = tab
        self.start_frame = None
        self.is_first_request = True
        self.html_content = None
        self.json_not_loaded = None
        self.json_loaded = None
        self.load_time = None
        self.frame_tree = None
        self.data = None

    def frame_started_loading(self, frameId):
        if not self.start_frame:
            self.start_frame = frameId
        self.tab.Performance.enable()
        self.json_not_loaded = self.tab.Performance.getMetrics()
        self.frame_tree = self.tab.Page.getFrameTree()
        self.tab.Network.setCacheDisabled(cacheDisabled=True)

        with open("results/preload.json", "w") as file: # generation metrics of starting loading
            json.dump(self.json_not_loaded, file)

    def frame_stopped_loading(self, frameId):
        self.json_loaded = self.tab.Performance.getMetrics()

        with open("results/onload.json", "w") as file: # generation metrics of starting loading
            json.dump(self.json_loaded, file)

        pdf = self.tab.Page.printToPDF() # generation PDF file

        with open("results/%s.pdf" % time.time(), "wb") as file:
            file.write(base64.b64decode(pdf['data']))

        temp_data = "starting_load" + json2html.json2html.convert( # generation HTML table from json file with metrics
            json=self.json_not_loaded) + "loaded" + json2html.json2html.convert(json=self.json_loaded)
        with open("results/table.html", "w") as file1:
            file1.write(temp_data)

        self.load_time = str( # generating a time-value for the page load speed in seconds
            self.json_loaded['metrics'][0]['value'] - self.json_not_loaded['metrics'][0]['value']) + " - Time to load (sec)"
        with open("results/time_to_load.txt", "w") as file:
            file.write(str(self.load_time))

        with open("results/frame_tree.txt", "w") as file:
            file.write(str(self.frame_tree))

        if self.start_frame == frameId:
            self.tab.Page.stopLoading()
            result = self.tab.Runtime.evaluate(expression="document.documentElement.outerHTML")
            self.html_content = result.get('result', {}).get('value', "")
            self.data = self.html_content

            self.tab.stop()

        with open("results/index.html", "w") as file: # generating html page into index.html
            file.write(self.data)


def close_all_tabs(browser):
    if len(browser.list_tab()) == 0:
        return

    for tab in browser.list_tab():
        try:
            tab.stop()
        except pychrome.RuntimeException:
            pass

        browser.close_tab(tab)

    time.sleep(1)
    assert len(browser.list_tab()) == 0


def main():
    files = glob.glob('results/*')
    for f in files:
        os.remove(f)

    if os.path.isdir('results'):
        os.rmdir('results')
    os.mkdir('results')

    browser = pychrome.Browser()

    # close_all_tabs(browser)

    tabs = []
    for i in range(1):
        tabs.append(browser.new_tab())

    for i, tab in enumerate(tabs):
        eh = EventHandler(browser, tab)

        tab.Page.frameStartedLoading = eh.frame_started_loading
        tab.Page.frameStoppedLoading = eh.frame_stopped_loading

        tab.start()
        tab.Page.stopLoading()
        tab.Page.enable()
        tab.Network.enable()

        # tab.Fetch.enable(enabled=False)
        tab.Page.navigate(url="https://sbis.ru/ofd")

    for tab in tabs:
        tab.wait(60)
        tab.stop()
        browser.close_tab(tab)

    print('Done')


if __name__ == '__main__':
    main()
