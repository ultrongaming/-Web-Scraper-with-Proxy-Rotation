import aiohttp
import asyncio
import random

class ProxyRotatingScraper:
    def __init__(self, proxies, headers=None):
        self.proxies = proxies
        self.headers = headers or {"User-Agent": "Mozilla/5.0"}

    async def fetch(self, session, url, proxy):
        try:
            async with session.get(url, proxy=proxy, timeout=10) as response:
                return await response.text()
        except Exception as e:
            return f"Error with proxy {proxy}: {e}"

    async def scrape(self, url):
        proxy = random.choice(self.proxies)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            return await self.fetch(session, url, proxy)

async def main():
    proxies = [
        "http://51.159.115.233:3128",
        "http://198.46.191.236:8080",
        "http://159.89.132.167:8989"
    ]
    scraper = ProxyRotatingScraper(proxies)
    urls = [
        "https://httpbin.org/ip",
        "https://example.com",
        "https://jsonplaceholder.typicode.com/posts/1"
    ]
    tasks = [scraper.scrape(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result[:200])

asyncio.run(main())