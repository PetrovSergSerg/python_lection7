from model.group import Group
from model.utils import random_string

testdata = [
    Group(name="name", header="header", footer="footer")
] + [
    Group(name="" if name else random_string("name", 10),
          header="" if header else random_string("header", 20),
          footer="" if footer else random_string("footer", 20))
    for name in [True, False]
    for header in [True, False]
    for footer in [True, False]
]
