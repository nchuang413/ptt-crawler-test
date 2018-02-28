#!/usr/bin/env python
# coding: utf-8
import re

import requests

import time

DATA_PATH = 'C:/ptt_BeautySalon_data'
CRAWL_PAGE_CNT = 10
URL_TEMPLATE = "https://www.ptt.cc/bbs/BeautySalon/index{}.html"
HOST = "https://www.ptt.cc"


def get_w_cookie(url):
    """GET HTTP url with custom header containing cookie info for PTT

    Parameters
    ----------
    url : str
        如：https://www.ptt.cc/bbs/BeautySalon/index2281.html

    Returns
    -------
    Response
        Requestsµ模組的Response Object
    """
    custom_headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36;"
    }

    resp = requests.get(url, headers=custom_headers)
    return resp


def get_total_page_cnt():
    """取得現在ptt板塊的總頁數

    Parameters
    ----------

    Returns
    -------
    int
       現在ptt板塊的總頁數
    """
    url = URL_TEMPLATE.format('')
    resp = get_w_cookie(url)

    # 這個符號
    # ‹-> &lsaquo;
    total_page_cnt = int(re.findall('href="/bbs/BeautySalon/index(\d+).html">&lsaquo; 上頁', resp.text)[0]) + 1
    return total_page_cnt

def get_list_page(url):
    """GET列表頁，取得內文頁的連結們

    Parameters
    ----------
    url : str
        PTT 列表頁URL

    Returns
    -------
    list
       PTT內文頁的links
    """
    resp = get_w_cookie(url)
    links = re.findall('<a href="(/bbs/BeautySalon/M.+\.html)">.+</a>', resp.text)
    detail_page_links = [HOST + link for link in links]
    return detail_page_links

def dump_page(url):
    """GET url的HTML並且寫到檔案裡

    Parameters
    ----------
    url : str
        PTT 內文頁URL

    Returns
    -------
    str
       儲存的檔案名稱
    """
    filename = "_".join(url.split('/')[-1].split('.')[:-1]) + '.html'
    resp = get_w_cookie(url)

    with open(DATA_PATH + '/' + filename, 'w', encoding='utf-8') as f:
        f.write(resp.text)
    return filename

if __name__ == "__main__":
    """
    以下的code只有被單獨跑的時候才會執行
    被import的時候不會執行
    """
    total_page_cnt = get_total_page_cnt()

    for pg in range(total_page_cnt, total_page_cnt - CRAWL_PAGE_CNT, -1):
        url = URL_TEMPLATE.format(pg)
        for link in get_list_page(url):
            print(link)
            dump_page(link)
            time.sleep(0.5)

