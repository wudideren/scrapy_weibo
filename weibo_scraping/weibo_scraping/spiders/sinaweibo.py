# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Request

from weibo_scraping.items import WeiboScrapingItem

class SinaweiboSpider(scrapy.Spider):
    name = 'sinaweibo'
    #allowed_domains = ['weibo.com']
    #start_urls = ['http://weibo.com/']

    def __init__(self):
        self.cookie = {
            'SCF' : 'AhcpPU3vmlbK6cgKdYsmyuAfOhZuqRumDzk6t3O6-0oE-GTLaxFIRu0Gch98TNDDG2MU5_XqKsoQgyY-vlWC2AE.',
            'SUBP' : '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWppxl40gGAeHpzfdNfQzhE5JpX5K-hUgL.Fo-RS0zEShncShe2dJLoIE.LxK-LB--L1hnLxKqL122LBKBLxKqL1hBL1-qLxK-L122LBKnESKq4SBtt',
            '_T_WM' : 'd1e8b0745e15bcea2201ec0928e4195d; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F',
            'SUB' : '_2A25w3iY3DeRhGeNN41ES-S_Iyz-IHXVQIUp_rDV6PUJbkdAKLUemkW1NSYRxjRTxsf7eJlnb52Bp7kV4_3tdz15h',
            'SUHB' : '0WGciC7EDIKb_c',
            'SSOLoginState' : '1574590055'
        }
        self.header = {
            'referer' : 'https://passport.weibo.cn'
        }

    def start_requests(self):
        return [scrapy.Request('https://weibo.cn/comment/IhODKnDgl?uid=1642591402&rl=0#cmtfrm', callback=self.parse, cookies=self.cookie, headers=self.header)]

    def parse(self, response):

        selector = Selector(response)
        comment_selector_list = selector.xpath("//div[contains(@id, 'C')]")
        for index, comment_selector in enumerate(comment_selector_list):
            # create item
            item = WeiboScrapingItem()

            # extract user
            user_selector_list = comment_selector.xpath('./a[1]/text()')
            if len(user_selector_list) == 0:
                item['user'] = ''
            elif user_selector_list.extract()[0] == u'查看更多热门>>':
                self.log('invalid comment: index=' + str(index))
                continue
            else:
                item['user'] = user_selector_list.extract()[0]

            # extract comment
            selector_list = comment_selector.xpath('./span[@class="ctt"]/text()')
            if len(selector_list) == 0:
                item['comment'] = ''
                continue
            elif selector_list.extract()[0] == u'回复':
                self.log('reply: index=' + str(index))
                continue
            else:
                item['comment'] = selector_list.extract()[0]

            # extract support_number
            support_number_selector_list = comment_selector.xpath('./span[last() - 2]/a/text()')
            if len(support_number_selector_list) == 0:
                item['support_number'] = 0
            else:
                item['support_number'] = support_number_selector_list.re('[0-9]+')[0]

            # extract date
            date_selector_list = comment_selector.xpath('./span[last()]/text()')
            if len(date_selector_list) == 0:
                item['date'] = ''
            else:
                item['date'] = date_selector_list.extract()[0]

            # return item
            yield item

        # scraping next page
        #next_page_selector_list = selector.xpath('//*[@id="pagelist"]/form/div/a/text()')
        #self.log('next page number:' + str(len(next_page_selector_list)))
        #self.log(next_page_selector_list.extract()[0])
        #self.log(next_page_selector_list.extract()[0] == u'下页')
        if  selector.xpath('//*[@id="pagelist"]/form/div/a/text()').extract()[0] == u'下页':
            #self.log('next page:' + next_page_selector_list.extract()[0])
            next_href = selector.xpath('//*[@id="pagelist"]/form/div/a/@href').extract()[0]
            yield Request('https://weibo.cn' + next_href, callback=self.parse)





