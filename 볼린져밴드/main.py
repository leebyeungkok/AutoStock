"""
볼린져밴드 구하기
"""
import requests
import json
import time
import math
import numpy as np

chartInfo60m = [{'price':61800, 'high':62300, 'low':61100},
    {'price':61500, 'high':61500, 'low':60400},
    {'price':60400, 'high':61000, 'low':59900},
    {'price':61000, 'high':61500, 'low':60600},
    {'price':61100, 'high':61600, 'low':60800},
    {'price':60800, 'high':61200, 'low':60400},
    {'price':60500, 'high':61200, 'low':59900},
    {'price':60500, 'high':61200, 'low':60300},
    {'price':60400, 'high':61100, 'low':59900},
    {'price':60700, 'high':60700, 'low':59600},
    {'price':59000, 'high':59400, 'low':57900},
    {'price':58200, 'high':58800, 'low':57600},
    {'price':57800, 'high':58000, 'low':55600},
    {'price':55400, 'high':56000, 'low':54500},
    {'price':55500, 'high':56100, 'low':55200},
    {'price':55300, 'high':56200, 'low':55300},
    {'price':56600, 'high':57600, 'low':56400},
    {'price':58100, 'high':58400, 'low':57900},
    {'price':57900, 'high':58100, 'low':57700},
    {'price':58100, 'high':58400, 'low':57700}]
"""
볼린져밴드 20,2 일경우 
"""
price = []
chart60m =[]
new60m = []
for index, info in enumerate(chartInfo60m):
    price = info.get('price')
    chart60m.append(price)
avg = np.mean(chart60m)
pyuncha = np.std(chart60m)
bldown20 = avg - pyuncha * 2.0
blup20 = avg + pyuncha * 2.0
print ('CENTER:', avg, '  DOWN:', bldown20, '  UP:', blup20)
