"""
매수/ 매도 
"""
import requests
import json
import time
import math
import numpy as np
from datetime import datetime, timedelta



jong = []
order = []
url = 'https://openapi.koreainvestment.com:9443'
file = open('acntNo.txt', 'r')
acntNo = file.read()
file.close()

file = open('appKey.txt', 'r')
appKey = file.read()
file.close()

file = open('appSecret.txt', 'r')
appSecret = file.read()
file.close()
hashKey = ''
headers = { "content-type":"application/json",
'appKey': appKey,
'appSecret': appSecret}

dtNow = datetime.now()
dtNowStr = str(dtNow.date()).replace('-','')
dtEnd = str(dtNow.date()).replace('-','')
dtStart = dtNow + timedelta(days=-90)
dtStart = str(dtStart.date()).replace('-','')
print(dtStart + '~' + dtEnd)



#######################################################################


# HashKey
def getHashKey(datas):
    sendUrl = url + '/uapi/hashkey'
    #print(sendUrl)
    res = requests.post(sendUrl, headers=headers, data=json.dumps(datas))
    #print(res)
    #print(res.json()['HASH'])
    hashKey = res.json()['HASH']
    #print('hashKey', hashKey);
    return hashKey

# 예약매수 매도 
def orderPreserve(iscd, qty, price, buySellCd):
    #print('#예약매수/매도')
    #print('hashKey', hashKey)
    
    bodyOrder = {
        'CANO':acntNo,
        'ACNT_PRDT_CD':'01',
        'PDNO': iscd,
        'ORD_QTY': qty,
        'ORD_UNPR': price,
        'SLL_BUY_DVSN_CD': buySellCd, # 01:매도, 02: 매수
        'ORD_DVSN_CD': '00', # 지정가 
        'ORD_OBJT_CBLC_DVSN_CD':'10', #현금
        'LOAN_DT':'',
        'RSVN_ORD_END_DT':'',
        'LDNG_DT': ''
      
    }
    headersOrder = { 
        "content-type":"application/json",
        'appKey': appKey,
        'appSecret': appSecret,
        'hashKey': getHashKey(bodyOrder),
        'authorization': 'Bearer ' + accessToken,
        'tr_id':'CTSC0008U',
        'tr_cont':'',
        'custtype':'P',
        
    }
    sendUrl = url +'/uapi/domestic-stock/v1/trading/order-resv'

    res = requests.post(sendUrl, headers=headersOrder, data=json.dumps(bodyOrder))
    #res = requests.post(sendUrl, headers=headersDaily, data=json.dumps(params))
    #print(res)
    #print(res.headers)
    #print(res.json())
    rtCd = res.json()['rt_cd']
    if rtCd != '0':
        print(rtCd, res.json()['msg1'])
    #output = res.json()['output']
    return res.json()

def getQty(price, amt, totQty):
    if amt < baseNum['minOrderAmt']: # 10만원 이하일 경우 10만원으로 계산한다. (최소금액)
        amt = baseNum['minOrderAmt'] 
    calcQty = math.ceil(amt/ price)
    if calcQty > int(totQty):
        calcQty = int(totQty)
    return calcQty

def getPrice(price, percent):
    
    chgPrice = price * (1+percent)
    if chgPrice < 1000:
        chgPrice = math.ceil(chgPrice)
    elif chgPrice < 5000: #5
        chgPrice = math.ceil(chgPrice)
        if chgPrice % 5 != 0:
            chgPrice = chgPrice + (5-chgPrice % 5) 
    elif chgPrice < 10000: #10
        chgPrice = math.ceil(chgPrice)
        if chgPrice % 10 != 0:
            chgPrice = chgPrice + (10-chgPrice % 10) 
    elif chgPrice < 50000: #50
        chgPrice = math.ceil(chgPrice)
        if chgPrice % 50 != 0:
            chgPrice = chgPrice + (50-chgPrice % 50) 
    elif chgPrice < 100000: #100
        chgPrice = math.ceil(chgPrice)
        if chgPrice % 100 != 0:
            chgPrice = chgPrice + (100-chgPrice % 100) 
    elif chgPrice < 500000: #500
        chgPrice = math.ceil(chgPrice)
        if chgPrice % 500 != 0:
            chgPrice = chgPrice + (500-chgPrice % 500)             
    else: # 50만원 이상
        chgPrice = math.ceil(chgPrice)
        if chgPrice % 1000 != 0:
            chgPrice = chgPrice + (1000-chgPrice % 1000)
    #    print('10만원이 넘는 종목은 포함하실 수 없습니다.');
    #    quit() 
    return chgPrice

def readFile(fileName):
    f = open(fileName, 'r')
    data = ''
    while True:
        line = f.readline()
        if not line: break
        data = data + line
    f.close()
    return json.loads(data)
#######################################################################


jsonData = readFile('baseData' + dtNowStr + '.json')
for index, item in enumerate(jsonData):
    print(item['name'] + ' ' + str(item['st']) + ' ' + str(item['rate']) + ' ' + item['updateDate'])



# 인증키
print("인증키가져오기#########################")
 
body = {"grant_type":"client_credentials",
        "appkey":appKey, 
        "appsecret":appSecret}

sendUrl = url + '/oauth2/tokenP'
res = requests.post(sendUrl, headers=headers, data=json.dumps(body))
#print(res)
#print(res.json())
accessToken = res.json()['access_token']
#time.sleep(1)

jong = []
for item in jsonData:
    jong.append(item)


# 정리된 종목을 보여주고 매수냐 매도냐를 판단한다. 

for index, item in enumerate(jong):
    # 매도조건
    if item['qty']> 0:
        if item['bfSt'] <= 80 and item['st'] > 80:
            item['sellQty'] =  item['qty']
        else:
            item['sellQty'] = 0
    else: 
        item['sellQty'] =0
    if item['stBf'] >= 50 and item['st'] < 50:
        item['buyQty'] =  10
    else :
        item['buyQty'] =  0


print('구분 : 종콕코드 | 종목명 | 수량 | 가격 | 금액 ')

for item in jong:
    if item['buyQty'] > 0:
        print('BUY' + ' : ' + item['iscd']+ ' | ' + item['name'] + ' | ' +  ' | ' + format(item['buyQty'],',') + ' | ' +  format(item['price'],',') + ' | ' +  format(item['buyQty'] * item['price'],','))
    if item['sellQty'] > 0:
        print('SELL' + ' : ' + item['iscd']+ ' | ' + item['name'] + ' | ' + ' | ' + format(item['sellQty'],',') + ' | ' +  format(item['price'],',')  + ' | ' +  format(item['sellQty'] * item['price'],','))
time.sleep(1);   


#orderPreserve(iscd, qty, price, buySellCd)
###############################################################################
inputOrder = input('Press O to order,  Other keys to quit')

if inputOrder == 'O' or inputOrder == 'o':
    print('Start Order Good luck!! =============================================')
    for item in jong:
        if item['buyQty'] > 0:
            resOrder = orderPreserve(item['iscd'], item['buyQty'], item['price'], '02') # 매수
            print(resOrder['rt_cd'] + ' : ' + item['iscd']+ ' | ' + item['name'] + ' | ' + ' | ' + format(item['buyQty'],',') + ' | ' +  format(item['price'],',') + ' | 매수')
            time.sleep(0.5)
        if item['sellQty'] > 0:
            resOrder = orderPreserve(item['iscd'], item['sellQty2'], item['price'], '01') # 매도
            print(resOrder['rt_cd'] + ' : ' + item['iscd']+ ' | ' + item['name'] + ' | ' + ' | ' + format(item['sellQty'],',') + ' | ' +  format(item['price'],',') + ' | 매도')
            time.sleep(0.5)
    print('End  Order =============================================')
else:
    print("Exit")
    quit()



