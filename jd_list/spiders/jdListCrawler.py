import scrapy
from scrapy_redis.spiders import RedisSpider
from jd_list.items import JdListLoader
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from redis import Redis



class jdListCrawler(scrapy.Spider):
    name='getGoodsList'
    # redis_keys = 'jdlist:start_urls'

    def __init__(self):
        super(jdListCrawler, self).__init__()
        self.start_urls = ['https://list.jd.com/list.html?cat=9987,653,655']
        self.allowed_domain = ['jd.com']
        # domain = kargs.pop('domain','')
        # self.allowed_domains = filter(None,domain.split(','))
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(5)  # throw a TimeoutException when thepage load time is more than 5 seconds.
        # super(jdListCrawler, self).__init__(*args,**kargs)



    def parse(self,response):
        jd = JdListLoader(response=response)
        urls = []
        self.driver.get(response.url)
        # redis = Redis()
        while True:
            wait = WebDriverWait(self.driver,2)
            wait.until(lambda driver:driver.find_elements_by_xpath('//div[@class="container"]//li[@class="gl-item"]//div[@class="p-img"]//img/src'))
            sel_list = self.driver.find_elements_by_xpath("//div[@class='container']//li[@class='gl-item']")
            url_list = [sel.get_attribute("href") for sel in sel_list]
        # for sel in self.find_elements_by_xpath('//div[@class="p-name"]/a').driver.find_elements_by_xpath("//div[@class='container']//li[@class='gl-item']//div[@class='p-name']/a"):
        #         url = sel.find_elements_by_xpath('//div[@class="container"]//div[@class="p-name"]/a').get_attribute('href')
        #         if url not in None:
        #             redis.lpush('jdlist:start_urls',url)
        #             urls.append(url)
        #         yield
            urls |= set(url_list)

            try:
                wait = WebDriverWait(self.driver,2)
                wait.until(lambda driver: driver.find_element_by_xpath('//div[@class="page"]//a[@class="pn-next"]'))
                next_page = self.driver.find_element_by_xpath('//div[@class="page"]//a[@class="pn-next"]')
                next_page.click()

            except:
                print "-------has arrived the last page----------"
                break

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_content)





    # def parse_content(self,response):








