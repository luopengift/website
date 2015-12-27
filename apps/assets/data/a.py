import sys
import json

sys.path.append('/data/app/website')
from models.mongodb import *
with open('ec2InstanceType.dat','r') as r:
    data = r.read()

data = eval(data)
for k in data:
    print k
    break


