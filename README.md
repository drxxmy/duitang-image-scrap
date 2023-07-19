# duitang-image-scrap

[![built with Python](https://img.shields.io/badge/Made%20with-Python3-red?style=for-the-badge&logo=python)](https://www.python.org/)
[![built with BeautifulSoup](https://img.shields.io/badge/Made%20with-BeautifulSoup-blue?style=for-the-badge&logo=bs4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

This python3 program is used to scrap images from duitang without official API.

### How to run a script

```bash
python run.py
```

### Example of script usage

```
python run.py

Enter a keyword to search for images: 水
Enter the page load depth in scroll numbers: 5
Enter the sleep timer after scrolling: 2
Running a script for 'http://www.duitang.com/search/?kw=水&type=feed', keyword is '水'
Browser window is open.
Performed scrolling 1 time(s).
Performed scrolling 2 time(s).
Performed scrolling 3 time(s).
Performed scrolling 4 time(s).
Performed scrolling 5 time(s).
Successfully obtained links to individual image pages - 84 links!
(1/84) | Getting the source image from the page!
(2/84) | Getting the source image from the page!
(3/84) | Getting the source image from the page!
(4/84) | Getting the source image from the page!
...
```
