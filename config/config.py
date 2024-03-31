from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class OpenAIAPI:
    api_key: str


@dataclass
class Config:
    tg_bot: TgBot
    openai_api: OpenAIAPI


def load_config():
    env = Env()
    env.read_env()
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  openai_api=OpenAIAPI(api_key=env('OPENAI_API_KEY')))
