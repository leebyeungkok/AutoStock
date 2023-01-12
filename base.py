"""
종목조회 기본데이터 만듦
"""
import requests
import json
import time
import math
import numpy as np
from datetime import datetime, timedelta


jongTarget = [
    { 'num':	1	,'iscd':'200350', 'name':'래몽래인' },
    { 'num':	2	,'iscd':'950130', 'name':'엑세스바이오'},
    { 'num':	3	,'iscd':'198440', 'name':'고려시멘트'},
    { 'num':	4	,'iscd':'219420', 'name':'링크제니시스'},
    { 'num':	5	,'iscd':'215480', 'name':'토박스코리아'},
    { 'num':	6	,'iscd':'037070', 'name':'파세코'},
    { 'num':	7	,'iscd':'139670', 'name':'키네마스터'},
    { 'num':	8	,'iscd':'030960', 'name':'양지사'},
    { 'num':	9	,'iscd':'189300', 'name':'인텔리안테크'},
    { 'num':	10	,'iscd':'026150', 'name':'특수건설'},
    { 'num':	11	,'iscd':'014970', 'name':'삼륭물산'},
    { 'num':	12	,'iscd':'014910', 'name':'성문전자'},
    { 'num':	13	,'iscd':'234100', 'name':'폴라리스세원'},
    { 'num':	14	,'iscd':'051380', 'name':'피씨디렉트' },
    { 'num':	15	,'iscd':'101360', 'name':'이엔드디'},
    { 'num':	16	,'iscd':'900120', 'name':'씨케이에이치' },
    { 'num':	17	,'iscd':'004720', 'name':'팜젠사이언스' },
    { 'num':	18	,'iscd':'196700', 'name':'웹스'},
    { 'num':	19	,'iscd':'041020', 'name':'폴라리스오피스'},
    { 'num':	20	,'iscd':'027580', 'name':'상보' },
    { 'num':	21	,'iscd':'114630', 'name':'폴라리스우노'},
    { 'num':	22	,'iscd':'067630', 'name':'HLB생명과학' },
    { 'num':	23	,'iscd':'203400', 'name':'에이비온'},
    { 'num':	24	,'iscd':'051160', 'name':'지어소프트' },
    { 'num':	26	,'iscd':'073570', 'name':'WI' },
    { 'num':	27	,'iscd':'074610', 'name':'이엔플러스'},
    { 'num':	28	,'iscd':'222160', 'name':'바이옵트로'},
    { 'num':	29	,'iscd':'003720', 'name':'삼영화학' },
    { 'num':	30	,'iscd':'153460', 'name':'네이블' },
    { 'num':	31	,'iscd':'121850', 'name':'코이즈'},
    { 'num':	32	,'iscd':'032820', 'name':'우리기술' },
    { 'num':	33	,'iscd':'101140', 'name':'인바이오젠'},
    { 'num':	34	,'iscd':'203650', 'name':'드림시큐리티'},
    { 'num':	35	,'iscd':'076080', 'name':'웰크론한텍'},
    { 'num':	36	,'iscd':'016920', 'name':'카스' },
    { 'num':	37	,'iscd':'006110', 'name':'삼아알미늄'},
    { 'num':	38	,'iscd':'094940', 'name':'푸른기술'},
    { 'num':	39	,'iscd':'031860', 'name':'엔에스엔'},
    { 'num':	40	,'iscd':'003580', 'name':'HLB글로벌' },
    { 'num':	41	,'iscd':'020120', 'name':'키다리스튜디오'},
    { 'num':	42	,'iscd':'109820', 'name':'진매트릭스' },
    { 'num':	43	,'iscd':'094360', 'name':'칩스앤미디어'},
    { 'num':	44	,'iscd':'256840', 'name':'한국비엔씨'},
    { 'num':	45	,'iscd':'054090', 'name':'삼진엘앤디'},
    { 'num':	46	,'iscd':'023150', 'name':'MH에탄올' },
    { 'num':	47	,'iscd':'224110', 'name':'에이텍티앤'},
    { 'num':	48	,'iscd':'230980', 'name':'에이트원' },
    { 'num':	49	,'iscd':'101670', 'name':'코리아에스이'},
    { 'num':	50	,'iscd':'189860', 'name':'서전기전'  }]
   

def writeFile(fileName, data):
    f = open(fileName, 'w')
    f.write(json.dumps(data))
    f.close()

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

inputDate = input('다른 날짜를 입력하시겠습니까? C to Continue, Q to quit, date = date   >>> ')

if inputDate == 'C'  or inputDate == 'c' or inputDate == '':
    print("continue")
elif inputDate == 'Q'  or inputDate == 'q':
    quit()
else:
    dtEnd = inputDate
    print(dtStart + '~' + dtEnd)
    inputTemp = ('any key to continue...')

# 함수정의 #######################################################################

# 일자별시세 --------------------------------------
def getDays30(iscd):
    print("일자별시세###################")
    headersDaily = { 
        "content-type":"application/json",
        'appKey': appKey,
        'appSecret': appSecret,
        'authorization': 'Bearer ' + accessToken,
        'tr_id':'FHKST01010400',
        'tr_cont':'',
        'custtype':'P',
        #'mac_address':macAddress
        }
    params = {
        'FID_COND_MRKT_DIV_CODE':'J',
        'FID_INPUT_ISCD': iscd,
        'FID_ORG_ADJ_PRC':'0',
        'FID_PERIOD_DIV_CODE':'D'
    }
    sendUrl = url +'/uapi/domestic-stock/v1/quotations/inquire-daily-price'
    res = requests.get(sendUrl, headers=headersDaily, params=params)
    #print(res)
    #print(res.headers)
    #print(res.json())
    output = res.json()['output']
    return output

# 기간별시세 --------------------------------------
def getPeriod(iscd, start, end):
    print("기간별시세###################")
    headersDaily = { 
        "content-type":"application/json",
        'appKey': appKey,
        'appSecret': appSecret,
        'authorization': 'Bearer ' + accessToken,
        'tr_id':'FHKST03010100',
        'tr_cont':'',
        'custtype':'P',
        #'mac_address':macAddress

        }
    params = {
        'FID_COND_MRKT_DIV_CODE':'J',
        'FID_INPUT_ISCD': iscd,
        'FID_INPUT_DATE_1':start,
        'FID_INPUT_DATE_2':end,
        'FID_PERIOD_DIV_CODE':'D',
        'FID_ORG_ADJ_PRC':'0'
    }
    sendUrl = url +'/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice'
    res = requests.get(sendUrl, headers=headersDaily, params=params)
    #print(res)
    #print(res.headers)
    #print(res.json())
    output = res.json()['output2']

    return output

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

# 계좌번호조회 ----------------------------------
def getAcntList(CTX_AREA_FK100, CTX_AREA_NK100):
    print("잔고조회##############")
    headersDaily = { 
        "content-type":"application/json",
        'appKey': appKey,
        'appSecret': appSecret,
        'authorization': 'Bearer ' + accessToken,
        'tr_id':'TTTC8434R',
        'tr_cont':'',
        'custtype':'P',
        'hashkey': hashKey
        #'mac_address':macAddress

        }
    params = {
        'CANO':acntNo,
        'ACNT_PRDT_CD':'01',
        'AFHR_FLPR_YN':'N',
        'OFL_YN':'',
        'INQR_DVSN':'02',
        'UNPR_DVSN':'01',
        'FUND_STTL_ICLD_YN':'N',
        'FNCG_AMT_AUTO_RDPT_YN':'N',
        'PRCS_DVSN':'00',
        'CTX_AREA_FK100':CTX_AREA_FK100,
        'CTX_AREA_NK100':CTX_AREA_NK100
    }
    sendUrl = url +'/uapi/domestic-stock/v1/trading/inquire-balance'
    res = requests.get(sendUrl, headers=headersDaily, params=params)
    return res

# 스토케스틱
def getStochestic(val, hVal, lVal):

    chart_history = []
    chart_h_history = []
    chart_l_history = []
    chart_max_history = []
    chart_min_history = []
    #try:

    for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]:
        chart_history.append(val[index:index + 5])
        chart_h_history.append(hVal[index:index + 5])
        chart_l_history.append(lVal[index:index + 5])
        #print(chart_h_history[index])
        chart_max_history.append(np.max(chart_h_history[index]))
        chart_min_history.append(np.min(chart_l_history[index]))


    # 스토캐스틱 %K (fast %K) = (현재가격-N일중 최저가)/(N일중 최고가-N일중 최저가) ×100
    st_kf_history = []
    for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                    26, 27, 28, 29, 30, 31, 32, 33, 34]:
        # print('***', chart_history[index], chart_min_history[index], chart_max_history[index])
        # print(index, '***', chart_history[index][0], chart_min_history[index],
        #      chart_max_history[index], (chart_history[index][0] - chart_min_history[index]) / (
        #                chart_max_history[index] - chart_min_history[index]) * 100)
        st_kf_history.append(
            (chart_history[index][0] - chart_min_history[index]) / (
                    chart_max_history[index] - chart_min_history[index]) * 100)

    # print('st_kf_history', st_kf_history)
    # 스토캐스틱 %D (fast %D) = m일 동안 %K 평균 = Slow %K
    st_k_history = []
    st_d_history = []
    for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                    26, 27, 28, 29, 30, 31, 32, 33, 34]:
        st_k_history.append(np.average(st_kf_history[index:index + 3]))
    
    #print('st_k_history', st_k_history)
    # slow %D = t일 동안의 slow %K 평균
    #for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
    #                26, 27, 28, 29, 30, 31, 32, 33, 34]:
    #    st_d_history.append(np.average(st_k_history[index:index + 15]))
        # print('st_d_history', st_d_history)
    #except:
    #    print("Unexpected error:", sys.exc_info())
    return st_k_history[0]

#######################################################################




# 인증키
body = {"grant_type":"client_credentials",
        "appkey":appKey, 
        "appsecret":appSecret}

sendUrl = url + '/oauth2/tokenP'
res = requests.post(sendUrl, headers=headers, data=json.dumps(body))
#print(res)
#print(res.json())
accessToken = res.json()['access_token']
#time.sleep(1)

# 계좌잔고 가져오기
acntData = getAcntList('','')
acntJson = acntData.json()
acntHeader = acntData.headers

if acntJson['rt_cd'] != '0':
    print("계좌가져오기 오류")
    print(acntJson)
    quit()

acntJsonOutput1 = acntJson['output1']
jongTemp = []
for item in acntJsonOutput1:
    jongTemp.append({
            'iscd': item['pdno'],
            'name': item['prdt_name'],
            'price': int(item['prpr']),
            'amto' : int(item['pchs_amt']),
            'amt': int(item['evlu_amt']),
            'profit': int(item['evlu_pfls_amt']),
            'qty':int(item['hldg_qty'])
        })

print("보유 제외종목##########################")
#print(jongTemp)
jongAll = []

for item in jongTarget:
    existJongTemp = False
    for item2 in jongTemp:
        if item['iscd'] == item2['iscd']:
            item['price'] = item2['price']
            item['amto'] = item2['amto']
            item['amt'] = item2['amt']
            item['profit'] = item2['profit']
            item['qty'] = item2['qty']
            existJongTemp = True
    jongAll.append(item)

for item in jongAll:
    if item.get('qty'):
        item['exist'] = True
    else: 
        item['qty'] = 0
        item['exist'] = False


# 종목별 일자별 시세
for index, item in enumerate(jongAll):
    chartValue = []
    chartHigh = []
    chartLow = []
    chartDate = []
    time.sleep(0.3)
    #print(str(item['num'])+ ': ' + item['name'])
    #print(item)
    chartData = getPeriod(item['iscd'], dtStart, dtEnd)
    #chartData = getDays30(item['iscd'])
    for item2 in chartData:
        #print('>>>',item2)
        chartDate.append(item2['stck_bsop_date'])
        chartValue.append(int(item2['stck_clpr']))
        chartHigh.append(int(item2['stck_hgpr']))
        chartLow.append(int(item2['stck_lwpr']))
    


    item['rate'] = int((int(chartValue[0])-int(chartValue[1]))/int(chartValue[1]) * 1000)/1000
    item['price'] = int(chartValue[0])

    # stockestc 호출 
    bfChartValue = chartValue[1::]
    bfChartHigh = chartHigh[1::]
    bfChartLow = chartLow[1::]
    #print ('test', chartValue, bfChartValue)
    item['st'] = int(getStochestic(chartValue, chartHigh, chartLow) * 1000)/1000
    item['stBf'] = int(getStochestic(bfChartValue, bfChartHigh, bfChartLow) * 1000)/1000
    item['updateDate'] = dtEnd


print("일자별데이터, 계좌잔액 정리########################")
writeFile('baseData' + dtNowStr + '.json', jongAll)
#print(jongAll)

for index, item in enumerate(jongAll):
    print(item['name'] + ' ' + str(item['st']) + ' ' + str(item['rate']) + ' ' + item['updateDate'])