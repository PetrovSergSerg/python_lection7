from abc import ABC, abstractmethod
import model.utils as utils
from random import choice
import data.constants as c


class Phone(ABC):
    @abstractmethod
    def get_value(self) -> None:
        pass


class CompactCityPhone(Phone):
    def get_value(self) -> str:
        return f'7495{utils.get_random_word(c.NUMBERS, 7)}'


class FullCityPhone(Phone):
    def get_value(self) -> str:
        return f'+7(49{choice("5689")})' \
               f'{utils.get_random_word(c.NUMBERS, 3)}-' \
               f'{utils.get_random_word(c.NUMBERS, 2)}-' \
               f'{utils.get_random_word(c.NUMBERS, 2)}'


class FullMobilePhone(Phone):
    def get_value(self) -> str:
        return f'+7({choice(c.MOBILE_CODES)})' \
               f'{utils.get_random_word(c.NUMBERS, 3)}-' \
               f'{utils.get_random_word(c.NUMBERS, 2)}-' \
               f'{utils.get_random_word(c.NUMBERS, 2)}'


class CompactMobilePhone(Phone):
    def get_value(self) -> str:
        return f'7{choice(c.MOBILE_CODES)}' \
               f'{utils.get_random_word(c.NUMBERS, 7)}'
