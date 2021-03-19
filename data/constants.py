from .phone import CompactCityPhone, CompactMobilePhone, FullCityPhone, FullMobilePhone
import string

MOBILE_PHONE_TEMPLATES = [CompactMobilePhone(), FullMobilePhone()]
CITY_PHONE_TEMPLATES = [CompactCityPhone(), FullCityPhone()]
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']
NUMBERS = string.digits
MOBILE_CODES = ['903', '905', '906', '915', '916', '925', '926', '999']
ALPHABET = string.ascii_letters
SYMBOLS = string.ascii_letters + string.digits + string.punctuation + " " * 15
