# -*- coding: utf-8 -*-
import scrapy
import re
import json
import itertools
import datetime
from chunqiu.items import ChunqiuItem


class ChspiderSpider(scrapy.Spider):
    name = "CHSpider"
    allowed_domains = ["www.ch.com",
                       "https://ajax.springairlines.com", "https://flights.ch.com"]
    start_urls = (
        'https://ajax.springairlines.com/cache/js/modules/data/citydict-zh-cn.js?vs=2017022401',
    )

    def parse(self, response):
        # print response.body
        # with open("cn.js", "wb") as f:
        #     f.write(response.body)
        Now = datetime.datetime.now()
        days =7
        dateList = []
        for i in range(7):
            elta = datetime.timedelta(days=i)
            dateList.append((Now + elta).strftime('%Y-%m-%d'))
        # print dateList
        strJson = re.search(r"return.*?(\{\D*\})", response.body).group(1)
        cityJson = ''.join(strJson.split("//简繁"))
        cityDict = json.loads(cityJson[:-3])
        # print cityDict
        # codeList = cityDict.keys()
        codeList = ['CKG', 'ZQZ', 'MIG', 'ZYI', 'SIA', 'WDS', 'YCU', 'NNG', 'HSN', 'LYG', 'PZI', 'LYA', 'KHN', 'HSU', 'TAO', 'LYI', 'XIC', 'URC', 'WEH', 'HZH', 'LHW', 'XUZ', 'JIQ', 'JIX', 'HRB', 'TYN', 'WUZ', 'WUX', 'TGO', 'SQJ', 'JNG', 'LXA', 'SYX', 'HJJ', 'TSN', 'SHP', 'NGB', 'HDG', 'AEB', 'TCZ', 'YZY', 'MFM', 'ENH', 'SZX', 'WNZ', 'SZV', 'DLC', 'YTY', 'SHX', 'LJG', 'SHA', 'CSX', 'FOC', 'JGS', 'CZX', 'WUH', 'TEN', 'LZH', 'LZO', 'HLD', 'INC', 'KMG', 'CTU', 'XNT', 'KUS', 'ZJA', 'DOY', 'PEK', 'ZUH', 'ACX', 'HFE', 'XNN', 'JHG', 'CGO', 'XFN', 'CGD', 'TVS', 'CGQ', 'GGN', 'HET', 'XMN', 'NNY', 'DNH', 'JZH', 'KJH', 'SJW', 'YIW', 'HEK', 'BAD', 'HKG', 'JJN', 'IQN', 'NTG', 'TOX', 'BAS', 'YNJ', 'SWA', 'DIG', 'HYN', 'ZHA', 'SHE', 'HAK', 'CAN', 'YNZ', 'YNT', 'KOW', 'KWE', 'CHG', 'KWL', 'DAT', 'HIA', 'SGN', 'CYI', 'DYG', 'DYA', 'YIH', 'TNA', 'HGH', 'WXN', 'NZH', 'NKG', 'BHY']
        perList = list(itertools.permutations(codeList,2))
        print len(perList)
        url = "https://flights.ch.com/Flights/SearchByTime"
        for i in perList:
            for j in dateList:
                formdata = {"Currency":"0", "SType":"0", "Departure": cityDict[i[0]][1].encode("utf-8"), "Arrival": cityDict[i[1]][
                    1].encode("utf-8"), "DepartureDate": j, "ReturnDate": "None", "IsIJFlight": "False", "IsBg": "False", "IsEmployee": "False", "IsLittleGroupFlight": "False", "SeatsNum":"1", "ActId":"0", "IfRet": "False"}
                yield scrapy.FormRequest(url,
                                     formdata=formdata,meta={"FromCode":i[0],"ToCode":i[1],"DateTime":j},
                                     callback=self.parseSearch,dont_filter=True)
        # for j in dateList:
        #     formdata = {"Currency":"0", "SType":"0", "Departure": "上海", "Arrival": "深圳", "DepartureDate": j, "ReturnDate": "None", "IsIJFlight": "False", "IsBg": "False", "IsEmployee": "False", "IsLittleGroupFlight": "False", "SeatsNum":"1", "ActId":"0", "IfRet": "False"}
        #     yield scrapy.FormRequest(url,formdata=formdata,callback=self.parseSearch,dont_filter=True,meta={"FromCode":"i[0]","ToCode":"i[1]","DateTime":j})

    def parseSearch(self,response):
        
        if len(response.body) >200:
                item = ChunqiuItem()
                item["FromCode"] =response.meta["FromCode"]
                item["ToCode"] = response.meta["ToCode"]
                item["DateTime"] = response.meta["DateTime"]
                item["Value"] = response.body
                yield item

