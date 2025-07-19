import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://api.github.com",
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts/1"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [(url, fetch(session, url)) for url in urls]
        responses = await asyncio.gather(*[t for _,t in tasks])
        for i, res in enumerate(responses):
            print(f"Response {i+1}:\n{res[:100]}...\n")  # Print first 100 characters

# Run the event loop
asyncio.run(main())

