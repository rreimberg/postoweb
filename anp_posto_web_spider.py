

import scrapy

INITIAL_URL = 'http://www.anp.gov.br/postos/GeraExcel.asp'
INITIAL_URL = 'file:///home/rreimberg/Downloads/ANP%20-%20AC.xls'

CONSULTA_URL = 'http://www.anp.gov.br/postos/consulta.asp'
RESULTADO_URL = 'http://www.anp.gov.br/postos/resultado.asp'

FORMATED_CNPJ = '[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}-[0-9]{2}'


class PostoWebSpider(scrapy.Spider):
    name = 'posto_web'

    def starts_request(self):
        print 'entrou'
        return [scrapy.Request(INITIAL_URL,
                callback=self.parse_registered_list, method='GET')]

    def parse_registered_list(self, response):

        for td in response.selector.xpath('//table[2]//td'):
            if len(td.re(FORMATED_CNPJ)):
                cnpj = ''.join(td.re('[0-9]+'))
                yield scrapy.Request(
                    CONSULTA_URL,
                    callback=self.search_cod_inst,
                    method='POST',
                    body='sCnpj={}'.format(cnpj))

    def search_cod_inst(self, response):

        # response.selector.xpath('//input')

        import ipdb; ipdb.set_trace()
        # yield Cod_inst:"4547"

    def extract_real_data(self, response):
        yield {
            'title': response.css('h1 a::text').extract()[0],
            'votes': response.css('.question .vote-count-post::text').extract()[0],
            'body': response.css('.question .post-text').extract()[0],
            'tags': response.css('.question .post-tag::text').extract(),
            'link': response.url,
        }
