import sys
sys.path.append('/data/app/website')

from model import *

collect = 'server'



with open('examples/server.json','r') as r:
    cur = r.read()

aa = eval(cur)
print aa,type(aa)

insert(collect,aa)




