from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    bot: TgBot


def load_config(path: Optional[str] = None) -> Config:
    """Func loads config data"""
    env = Env()
    env.read_env(path)
    return Config(bot=TgBot(token=env("BOT_TOKEN"),
                            admin_id=env("ADMIN_ID")))
