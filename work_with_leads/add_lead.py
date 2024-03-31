import requests
import aiohttp


async def create_lead(webhook_url, lead_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=lead_data) as response:
            if response.status == 404:
                print("Ошибка: страница не найдена (404)")
                # Обработка ошибки 404
            elif response.status == 200:
                result = await response.json()
                # Обработка успешного ответа
            else:
                http_error = f"Ошибка HTTP: {response.status}"
                response_text = await response.text()
                print(http_error, response_text)
