# -*- coding: utf-8 -*-
import scrapy


class VeleirosSpider(scrapy.Spider):
    name = 'veleiros'
    #allowed_domains = ['lista.mercadolivre.com.br']
    start_urls = ['https://lista.mercadolivre.com.br/veiculos/nautica/veleiro-monocasco-e-multicasco/']
    #start_urls = ['https://lista.mercadolivre.com.br/veleiro#D[A:veleiro,L:undefined]/']
    #start_urls = ['https://lista.mercadolivre.com.br/energia-eletrica-solar-paineis-solares/']
    #start_urls = ['https://lista.mercadolivre.com.br/energia-eletrica-solar-paineis-solares-em-parana/painel-solar']
    def parse(self, response):
        items = response.xpath('//section[@id="results-section"]/ol[@id="searchResults"]/li[@class="results-item highlighted article grid "]')
        self.log('-----------------Quantidade de Registros: ' + str(len(items)) + '-----------------')

        for item in items:
            url = item.xpath('./div/a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)
        next_page = response.xpath('//div[contains(@class, "pagination__container")]//a[@class = "andes-pagination__link prefetch"]/@href')
        if next_page:
            self.log('Proxima pagina: %s' % next_page.extract_first())
            yield  scrapy.Request(
                url = next_page.extract_first(), callback=self.parse
            )

    def parse_detail(self, response):
        #self.log(response.xpath('//h1[@id="ad_title"]/text()').extract_first())
        title = response.xpath('//h1[@class="item-title__primary "]/text()').extract_first()
        price = response.xpath('//span[@class="price-tag-fraction"]/text()').extract_first()
        description = response.xpath('//div[@class="item-description__text"]/p[text()]').extract_first()
        yield {
            'title': title,
            'price': price,
            'description': description,
        }
