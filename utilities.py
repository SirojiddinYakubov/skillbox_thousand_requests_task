import aiohttp
import asyncio
from tqdm import tqdm
import validators


class Request(object):
    def __init__(self, count):
        self.count = count

    async def get_variables(self):
        url = input('Введите URL-адрес: ')
        if validators.url(url):
            await self.load_tasks(count=self.count, url=url)
        else:
            print('URL введен в неправильном формате')
            await self.get_variables()

    async def load_tasks(self, count=0, url=None):
        try:
            tasks = []
            if url:
                async with aiohttp.ClientSession() as session:
                    request = await self.create_request(session=session, url=url)
                    if request:
                        for _ in tqdm(range(count), unit=' tasks', desc='Подготовка задач'):
                            task = asyncio.create_task(self.create_request(session=session, url=url))
                            tasks.append(task)
                        for _ in tqdm(range(len(tasks)), unit=' requests', desc=f'Запрос {url}'):
                            await asyncio.gather(*tasks)
                        print(f'На {url} успешно отправлено {count} запросов.')
                    else:
                        print('Cайт не существует или не может быть найден')
                        await self.get_variables()

            else:
                print('URL не введен')
        except Exception as e:
            print(e)

    async def create_request(self, session, url):
        try:
            async with session.get(url) as response:
                return response
        except Exception as e:
            print(e)


r = Request(count=1000)

