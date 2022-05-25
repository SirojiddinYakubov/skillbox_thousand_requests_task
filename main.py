from utilities import Request
import asyncio

if __name__ == '__main__':
    r = Request(count=1000)
    asyncio.run(r.get_variables())