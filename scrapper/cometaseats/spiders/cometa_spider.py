#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.selector import Selector
from cometaseats.items import CometaseatsItem
from scrapy import Request
from scrapy.http import FormRequest
from scrapy.shell import inspect_response
import json
import re

class CometaSpider(Spider):
    name = "cometaseats"
    allowed_domains = ["viacaocometa.com.br", "jcaholding.com.br"]
    start_urls = ["http://www.viacaocometa.com.br/pt/"]
    
    def parse(self, response):
        forms = Selector(response).xpath("/html/body/div[1]/div[3]/div[1]/div[1]/form")
        formAction = forms[0].xpath("@action").extract()[0]
        places = [("1", "73"),("1", "78"), ("1", "9"), ("1", "23"), ("1", "8"), ("1", "80"), ("1", "87"), ("1", "91"), ("1", "17"), ("1", "82"), ("1", "43"), ("5", "56"), ("23", "65")]
        dates = [("17/01/2017")]
        formdatas = []        
        for date in dates:
            for place1, place2 in places:
                formdatas.append({"origem": "", "destino": "", "dataInicial":date,"dataFinal":"","idioma":"pt", "origemCodigo": place1, "destinoCodigo": place2})
                formdatas.append({"origem": "", "destino": "", "dataInicial":date,"dataFinal":"","idioma":"pt", "origemCodigo": place2, "destinoCodigo": place1})
                
        for formdata in formdatas:
            request = FormRequest(formAction, method="POST", callback=self.parseSearch, formdata=formdata, dont_filter=True)
            yield request

    
    def parseSearch(self,response):
        request = Request("https://vendas.jcaholding.com.br/VendaWeb/consulta/idaJson/0", method="POST", callback=self.parseBusList, dont_filter=True)
        return [request]

    def parseBusList(self, response):
        jsonData = json.loads(response.body_as_unicode())
        buses = jsonData["lsConsultaIda"]
        for bus in buses:
            if bus['classe'] in ('CONV', 'EXEC', 'CONV C/AR', 'CONV. AR+', 'EXECUTIVO'):
                formdata = {"servicoIda": bus['servico']}
                request = FormRequest("https://vendas.jcaholding.com.br/VendaWeb/poltronas", method="POST", callback=self.parseBus, formdata=formdata, dont_filter=True)
                request.meta['data'] = bus
                yield request
                
    def parseBus(self, response):
        item = CometaseatsItem()
        item['seats'] = [0 for x in xrange(46)]
        item['data'] = response.meta['data']

        occupied_seats = Selector(response).xpath('//table[@class="cpo1"]/tr/td[@class="ocupada"]')
        for occupied_seat in occupied_seats:
            seat_id = occupied_seat.xpath("@id").extract()[0]
            seat = int(re.findall('\d+', seat_id)[0])
            item['seats'][seat - 1] = 1

        return [item]




