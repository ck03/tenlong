# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class TelSpider(scrapy.Spider):
    name = 'tel'
    allowed_domains = ['www.tenlong.com.tw']
    start_urls = ['https://www.tenlong.com.tw/tw']
    url_title = "https://www.tenlong.com.tw"
    n = 1
    print("天瓏爬蟲開始.....")

    def parse(self, response):
        li_list = response.xpath("//div[@class='sidebox'][1]/ul/li")
        for li in li_list:
            item = {}
            item["s_cate"] = li.xpath("./a/text()").extract_first()
            item["s_href"] = self.url_title + li.xpath("./a/@href").extract_first()

            # print(item)
            yield scrapy.Request(
                item["s_href"],
                callback=self.parse_book_list,
                meta={"item": deepcopy(item)}
            )

    def parse_book_list(self, response):
        item = deepcopy(response.meta["item"])
        # print(item)
        li_list = response.xpath("//div[@class='book-list book-list-event']/div/ul/li")
        for li in li_list:
            item["book_img"] = li.xpath("./a/img/@src").extract_first()
            item["book_href"] = self.url_title + li.xpath("./a/@href").extract_first()
            item["web_page"] = self.n
            yield scrapy.Request(
                item["book_href"],
                callback=self.parse_book_detail,
                meta={"item": deepcopy(item)}
            )
        # 翻頁
        next_url_str = response.xpath("//div[@class='pagination pagination-footer']/a[last()]/text()").extract_first()

        if next_url_str == "下一頁":
            # debug 用
            # self.n += 1
            # if self.n >= 3:
            #    return
            next_url = self.url_title + response.xpath(
                "//div[@class='pagination pagination-footer']/a[last()]/@href").extract_first()
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item": response.meta["item"]}
            )

    def parse_book_detail(self, response):
        item = deepcopy(response.meta["item"])
        bt = response.xpath("//div[@class='content']/div/div/h1/text()").extract_first()
        # 去除換行字符\n
        item["book_title"] = bt.strip()
        ba = response.xpath("//div[@class='content']/div/div/h3/text()").extract_first()
        item["book_author"] = ba.strip()
        li_list = response.xpath("//div[@class='content']/div[@class='item-info']/ul/li")
        for li in li_list:
            s = li.xpath("./span[1]/text()").extract_first()
            # print(s)
            if s == "出版商:":
                item["book_public"] = li.xpath("./span[last()]/a/text()").extract_first()
            elif s == "出版日期:":
                item["book_pub_date"] = li.xpath("./span[last()]/text()").extract_first()
            elif s == "定價:":
                item["book_orig_price"] = li.xpath("./span[last()]/text()").extract_first()
            elif s == "售價:":
                item["book_sale_price"] = li.xpath("./span[2]/span[1]/text()").extract_first() + \
                                          "折" + li.xpath("./span[2]/span[2]/text()").extract_first()
            elif s == "語言:":
                item["book_language"] = li.xpath("./span[last()]/text()").extract_first()
            elif s == "頁數:":
                item["book_page"] = li.xpath("./span[last()]/text()").extract_first()
            elif s == ":":
                s = li.xpath("./span[1]/acronym/text()").extract_first()
                if s == "ISBN-13":
                    item["book_jsbn13"] = li.xpath("./span[last()]/text()").extract_first()
        # print(item)
        yield deepcopy(item)

        # item["book_vip_price"] = response.xpath(
        #     "//div[@class='content']/div/ul/li[5]/span[2]/span[1]/text()").extract_first() + \
        #                           "折" + response.xpath(
        #     "//div[@class='content']/div/ul/li[5]/span[2]/span[2]/text()").extract_first()
