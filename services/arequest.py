import aiohttp
import asyncio

class ARequest:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def fetch(self, url, params=None, headers=None):
        async with self.session.get(url, params=params, headers=headers) as response:
            return await response.text()

    async def close(self):
        await self.session.close()

async def main():
    fetcher = ARequest()
    urls = [
        ("https://httpbin.org/get", {"test": "1"}, {"Custom-Header": "value"}),
        ("https://api.github.com", None, None)
    ]
    tasks = [fetcher.fetch(url, params, headers) for url, params, headers in urls]
    responses = await asyncio.gather(*tasks)

    await fetcher.close()
    print(responses)

if __name__ == "__main__":
    asyncio.run(main())

