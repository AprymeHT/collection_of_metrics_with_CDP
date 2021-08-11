# collection_of_metrics_with_CDP

A python test cases for the test problem using pychrome

## Table of Contents

* [Installation](#installation)
* [Setup Chrome](#setup-chrome)
* [Getting Started](#getting-started)
* [Results folder](#results-folder)
* [Ref](#ref)


## Installation

To install pychrome, simply:

```
$ pip install -U pychrome
```
To install json2html:
```
$ pip install json2html
```

## Setup Chrome


for the test1.py you have to use headless mode (chrome version >= 59):

```
$ google-chrome --headless --disable-gpu --remote-debugging-port=9222
```

for the test2.py you have to use simple mode:

```
$ google-chrome --remote-debugging-port=9222
```

## Getting Started

To test your site, you must change this line:

``` 
tab.Page.navigate(url="https://your.site")
```

Then execute any of py's files

After running the script, you will have a results folder with several files (depending on the running test) from 5 to 7
Files characterize different information about metrics

## Results folder

1. anySymbols.pdf: file that represents the pdf version of the site
2. frame_tree.txt: information about the Frame hierarchy
3. time_to_load.txt: includes information about loading times
4. preload.json: metric collected before page load
5. onload.json: metric collected after page load
6. table.html: this html page includes 2 tables with more readable information
7. index.html: includes all HTML text without any css/js code

## Ref

* [chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface/)
* [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/tot/)
