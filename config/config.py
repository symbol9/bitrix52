from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Webhooks:
    webhook: str
    webhook2: str


@dataclass
class GoogleSheetsAPI:
    api_key: str


@dataclass
class OpenAIAPI:
    api_key: str


@dataclass
class Config:
    tg_bot: TgBot
    openai_api: OpenAIAPI
    webhooks: Webhooks


def load_config():
    env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  openai_api=OpenAIAPI(api_key=env('OPENAI_API_KEY')),
                  webhooks=Webhooks(webhook=env('webhook_url'), webhook2=env('webhook_url2')))
