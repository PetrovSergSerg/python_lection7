from model.group import Group
from model.utils import random_string
import os.path
import jsonpickle
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of groups", "datafile"])
except:
    getopt.usage()
    sys.exit(2)

n = 5
f = "data/groups.json"

for name, value in opts:
    if name == "-n":
        n = int(value)
    elif name == "-f":
        f = value

testdata = [
               Group(name="" if name else random_string("name", 10),
                     header="" if header else random_string("header", 20),
                     footer="" if footer else random_string("footer", 20))
               for name in [True, False]
               for header in [True, False]
               for footer in [True, False]
           ] + [Group().set_random_parameters_to_random_value() for i in range(n)]

datafile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(datafile_path, "w") as datafile:
    jsonpickle.set_encoder_options("json", indent=2)
    datafile.write(jsonpickle.encode(testdata))
