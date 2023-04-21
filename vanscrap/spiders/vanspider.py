import scrapy
import re
from scrapy_splash import SplashRequest


class VanSpider(scrapy.Spider):
    """Spider class to extract information about vans from yescapa website.

    It cointains three main generators "start_requests()", "parse_link()" and
    "parse()". The name of the spider is "van".

    """

    name = 'van'
    page_number = 2

    def start_requests(self):
        """Call the SplashRequest to launch the Splash service.

        It renders an URL, in this case the Yescapa website.
        And it calls the "parse()" function.

        """
        url = 'https://www.yescapa.pt/s?longitude=-9.004669&latitude=39.193948&radius=146592&page=1'
        yield SplashRequest(url=url, callback=self.parse)

    def parse_link(self, response, **kwargs):
        """Parse the link for each item (van).

        It extracts information from the header, but as well technical 
        elements, owner conditions ans some information about the reviews.

        """
        item = kwargs['item']  # add elements from the "parse() function"

        # REGEX EXPRESSIONS
        regex_strong = '<strong>(.*?)<\/strong>'
        regex_strong_2 = r'<strong>(\s*[^<>\n]+\s*)</strong>'
        regex_span = r"""(?<=<span itemprop="brand">).*?(?=</span>)"""

        # HEADER ELEMENTS
        string_header = response.css('div.viewAd_header_icons').get()
        match_header = re.findall(regex_strong, string_header)
        match_header = [element.strip() for element in match_header]
        item['seats'] = match_header[0].split(' ')[0]
        item['sleep_places'] = match_header[1].split(' ')[0]
        item['driving_license'] = match_header[2][-1]
        item['international'] = match_header[3]
        item['animals'] = match_header[4]

        # TECHNICAL INFO ELEMENTS
        str_technical_model = response.css(
            'div.viewAd_technical_info_section').get()
        item['model'] = re.findall(
            regex_span, str_technical_model)[0].strip()
        str_technical_info = response.css('div.viewAd_technical').get()
        item['year'] = re.findall(
            regex_strong, str_technical_info)[0]
        item['weight (kg)'] = re.findall(
            regex_strong, str_technical_info)[1]
        item['fuel'] = re.findall(
            regex_strong, str_technical_info)[7]
        item['km'] = re.findall(
            regex_strong, str_technical_info)[10]
        item['tank (l)'] = re.findall(
            regex_strong_2, str_technical_info)[-2]\
            .split('\n')[1].split('litros')[0].strip()

        # OWNER CONDITIONS
        string_owner_conditions = response.css(
            'div.viewAd_ownerConditions').get()
        item['deposit (€)'] = re.findall(
            regex_strong_2, string_owner_conditions)[0]\
            .split('\xa0€')[0].split('\n')[-1].strip()
        item['deposit_payment_method'] = re.findall(
            regex_strong_2, string_owner_conditions)[1]\
            .split('\n')[1].strip()
        item['smoking'] = re.findall(
            regex_strong_2, string_owner_conditions)[3]

        # REVIEWS
        reviews_year = [] 
        for review in response.css('div.viewAd_reviews'):
            for element in review.css('div.reviewItem_content'):
                reviews_year.append(
                    element.css('span::text').get().split(' ')[1])

        item['most_reviews_year'] = max(
            set(reviews_year), key=reviews_year.count)

        yield item  # generator creates a dictionary

    def parse(self, response):
        """Generate main parsing.

        Main generator, that gets some information from the main page and saves
        it into adictionary. This dictionary is then saved into another
        dictionary that is later called on the "parse_link()" function.

        """
        items = response.css('article')  # parse each article HTML element
        for item in items:
            try:
                link = item.css('a::attr(href)').get()
                item_dict = {
                    'name': item.css('h2::text').get()
                    .replace('\n', '').strip(),
                    'location': item.css('p::text').get()
                    .replace('\n', '').strip(),
                    'rating': item.css('span.font-bold.text-black::text')
                    .get().replace('\n', '').strip(),
                    'reviews': item.css('span.text-gray-500::text')
                    .get().replace('(', '').replace(')', '').strip(),
                    'price (€)': str(item.css('p.leading-tight').get())
                    .split('€')[1].replace('\n', '')
                    .replace('\xa0', '').split(' ')[0],
                }
                yield SplashRequest(  # launch the Splash service
                    url=link,
                    callback=self.parse_link,
                    cb_kwargs={'item': item_dict})

            except Exception as e:
                print(e)

        # MULTIPLE PAGES
        next_page = f"https://www.yescapa.pt/s?longitude=-9.004669&latitude=39.193948&radius=146592&page={self.page_number}"
        if self.page_number <= 80:  # iterate over a max of 80 pages
            print('page done')
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)