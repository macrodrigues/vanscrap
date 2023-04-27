# Web Scraping with Scrapy and Splash

The project consists of scraping the [Yescapa](https://www.yescapa.pt/) website, to get data about motorhomes.

Since the website is dynamic, simple scraping wasn't possible. A Headless browser was needed to execute the JavaScript code. For this I used Splash, which can be easily integrated with Scrapy.

### Scrapy

It is an open-source fast web crawling and web scraping framework for Python. It includes built-in support for handling common web scraping tasks such as handling cookies, user agents, and pagination. Additionally, it provides a built-in mechanism for handling web page parsing using XPath and CSS selectors.

### Splash

It is a lightweight and open-source headless browser that is designed to render web pages and execute JavaScript code. You can launch it with Docker, and to use it with Scrapy, we need  [**Scrapy-Splash**](https://pypi.org/project/scrapy-splash/)  which uses Splash HTTP API.

Ge to know more about the flow of the project in my medium article:
<p  align="center">
<img  width="500"  src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Z02uV_be03OprLACopW2pQ.jpeg"  alt="scrpy image">
</p>
<h1 align="center"><a href="https://medium.com/@macrodrigues/web-scraping-with-scrapy-and-splash-3d5666ba78ff">Medium Article</a></h1>
