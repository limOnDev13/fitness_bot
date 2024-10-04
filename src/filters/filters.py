import logging
import re
from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message

logger = logging.getLogger("main.filter")


class PhoneFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        logger.debug("Input phone: %s", message.text)
        if message.text:  # mypy
            return re.search(r"(\+7|8)\d{10}", message.text) is not None
        else:
            return False


class DateFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            if message.text:
                logger.debug("Input date_time: %s", message.text)
                chosen_datetime: datetime = datetime.strptime(
                    message.text, "%d.%m.%Y %H:%M"
                )
                if chosen_datetime < datetime.now():
                    return False
                return True
            else:
                return False
        except ValueError:
            logger.warning("Invalid format")
            return False
