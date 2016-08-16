from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from urllib.request import urlopen
import random
import math
from django.template import loader, Context
from Tour.models import TripMain,Plan
from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def indexBingo(request):
    suggestList = []
    suggestList.append("行程名稱：三星訪古　大啖蔥蒜美食    行程詳述：天送埤文物室賞玩百件古農物→田媽媽蔥蒜美食館享用青蔥好味→參觀青蔥文化館、買伴手→天山休閒農場摸小豬、觀蝶螢")
    coup = "店家贈送特製免費冰棒"
    if 'area' in request.GET:
        try:
            bingoPanel = createBingoPanel(9,1,request.GET['area'])
            missionList = createMission(9)


        except:
            #bingoPanel = createBingoPanel(1, 1, request.GET['area'])
            return render_to_response('fail.html', locals())

    #suggestStr = parseSuggest("宜蘭", "三星")
    #suggestList.append(suggestStr[0])

    #for b in bingoPanel:
    #    addr = b.address
    #    areaName = addr[0:2]
    #    townName = addr[3:2]
    #    suggestStr = parseSuggest("宜蘭", "三星")
        # 得到此區的旅遊資料
        # 建議其他旅遊地點
        #ranNum = random.randint(0, len(suggestStr))
    #    selectOne = suggestStr[1]
    #    suggestList.append(selectOne)

    #tmpTest = suggestList[0]


    return render_to_response('Bingo.html',locals())


def createBingoPanel(gridNum, totalDay, area): #產生初始Bingo拼盤


    # create BingoArray GridNum  (Random Order)



    bingoObject = setPortion(gridNum, totalDay, area)

    listAll = []
    for i in bingoObject.hotelList:
        listAll.append(i)
    for i in bingoObject.spotList:
        listAll.append(i)
    for i in bingoObject.foodList:
        listAll.append(i)

    # 先統計總數量
    count = len(listAll)
    num_range = range(0, count)
    order = random.sample(num_range, count)

    listAllNewOrder = []
    for i in order:
        listAllNewOrder.append(listAll[i])



    # {名稱 / 地址 / 時間（可為NULL）/ 類型（景點、用餐、住宿）}

    #自動找圖找網址工具（？）

    return listAllNewOrder

def parseSuggest(area,town):

    u = urlopen('http://data.coa.gov.tw/Service/OpenData/EzgoSuggestTravel.aspx')
    resp = json.loads(u.read().decode('utf-8'))

    suggestList = []
    for index in range(1, len(resp)):

        cityName  = resp[index]["City"][0:2]
        townName = resp[index]["Town"][3:2]


        if(resp[index]["FirstDayTravel"] != "" and  townName == town):
            suggestList.append("行程名稱："+resp[index]["Name"] + "行程內容：" + resp[index]["FirstDayTravel"])
            #suggestList = suggestList + resp[index]["FirstDayTravel"]
        else:
            pass

        #if(resp[index]["SecondDayTravel"] != ""  and resp[index]["SecondDayTravel"] != False and cityName == area and townName == town):
        #    suggestList.append(resp[index]["SecondDayTravel"] and  cityName == area and townName == town)
        #    #suggestList = suggestList + resp[index]["SecondDayTravel"]
        #else:
        #    pass

        #if(resp[index]["ThirdDayTravel"] != "" and resp[index]["ThirdDayTravel"] != False and cityName == area and townName == town):
        #    suggestList.append(resp[index]["ThirdDayTravel"])
        #    #suggestList = suggestList + resp[index]["ThirdDayTravel"]
        #else:
        #    pass
    return suggestList

def pickHotel(count, area): #從Hotel JSON資訊取出部分

    u = urlopen('http://data.coa.gov.tw/Service/OpenData/EzgoTravelHotelStay.aspx')
    resp = json.loads(u.read().decode('utf-8'))
    # resp[0]["Name"]

    tourList = []
    for index in range(1, len(resp)):
        # print(resp[index]["name"])
        name = str(resp[index]["Name"])
        addr = str(resp[index]["Address"])
        # 篩選掉區域

        county = addr[0:2]
        if county == area:
            tmpTour = TourObject(name, addr,"hotel")
            tourList.append(tmpTour)
            # 篩選掉區域

    # 設定要選擇的區域
    tourListSelected = []
    num_range = range(0, len(tourList))
    result = random.sample(num_range, count)
    # result = random.sample(num_range, count)   正式用的
    for num in result:
        tmpObj = tourList[num]
        tourListSelected.append(tmpObj)
    return tourListSelected



def pickSpot(count, area): #從Spot JSON資訊取出部分

    u = urlopen('http://data.coa.gov.tw/Service/OpenData/EzgoMovingRoad.aspx')
    resp = json.loads(u.read().decode('utf-8'))
    #resp[0]["Name"]

    tourList = []
    for index in range(1,len(resp)):
        #print(resp[index]["name"])
        name = str(resp[index]["Name"])
        addr = str(resp[index]["AreaLocation"])
        #篩選掉區域

        county = addr[0:2]
        if county == area:
            tmpTour= TourObject(name,addr,"spot")
            tourList.append(tmpTour)
         # 篩選掉區域

    #設定要選擇的區域
    tourListSelected = []
    num_range = range(0, len(tourList))
    result = random.sample(num_range, count)
    #result = random.sample(num_range, count)   正式用的
    for num in result:
        tmpObj = tourList[num]
        tourListSelected.append(tmpObj)
    return tourListSelected

def pickFood(count, area): #從Food JSON資訊取出部分

    u = urlopen('http://data.coa.gov.tw/Service/OpenData/EzgoTravelFoodStay.aspx')
    resp = json.loads(u.read().decode('utf-8'))
    #resp[0]["Name"]

    tourList = []
    for index in range(1,len(resp)):
        #print(resp[index]["name"])
        name = str(resp[index]["Name"])
        addr = str(resp[index]["Address"])
        #篩選掉區域

        county = addr[0:2]
        if county == area:
            tmpTour= TourObject(name,addr,"food")
            tourList.append(tmpTour)
         # 篩選掉區域

    #設定要選擇的區域
    tourListSelected = []
    num_range = range(0, len(tourList))
    result = random.sample(num_range, count)
    #result = random.sample(num_range, count)   正式用的
    for num in result:
        tmpObj = tourList[num]
        tourListSelected.append(tmpObj)
    return tourListSelected



def setPortion(gridTotol, totalDay,area): #Hotel只能依天數設定 可設定餐飲及景點比例
    #                   hotel  spot  eat
    #預設配比  grid:9 ==>  1  x-1-4   4

    foodCount = totalDay * 4
    spotCount = gridTotol - foodCount - totalDay

    hotelList = pickHotel(totalDay, area)
    spotList = pickSpot(spotCount, area)
    foodList = pickFood(foodCount, area)

    bingoObj = BingoObject(hotelList,foodList,spotList)

    return bingoObj


class TourObject:
    def __init__(self, name, address, type ):
        self.name = name
        self.address = address
        self.type = type

class BingoObject:
    def __init__(self, hotelList, foodList, spotList):
        self.hotelList = hotelList
        self.foodList = foodList
        self.spotList = spotList


def fullPlan(request):
    trip = TripMain.objects.latest("TripName")
    planList = trip.plan_set.all()
    planList = planList.order_by('Order')
    tmp = planList[0]
    rowCountForList = 15

    return render_to_response('fullPlanPrint.html',locals())

def createTripMain():
    import time
    ts = time.time()
    TripMain.objects.create(TripName='trip'+str(ts))
    return 0;

def createPlan(planObject,order):

    name = planObject.name
    addr = planObject.address
    type = planObject.type
    newTripMain = TripMain.objects.latest("TripName")
    Plan.objects.create(trip = newTripMain, LocationName=name, Address = addr, Type= type, Order = order)
    return 0;

def createMission(count):
    mission = ["抓到三隻水系寶可夢","進化兩隻神奇寶貝","請一個不認識的人喝飲料","玩美食接龍（至少三個)","幫老闆做一件事（例如砍柴，打掃等）", "跟老闆拍照", "請一個路人幫忙老闆網站按讚","找到3個寶可夢補給站","寶可夢升級一等","在空地大喊「我愛小小兵」","跟老闆自拍打卡","跟老闆玩換臉自拍","買前一個顧客買的東西","在店門口請人拍空氣吉他影片"]
    num_range = range(0, len(mission))
    numRand = random.sample(num_range, count)
    result = []
    for n in numRand:
        result.append(mission[n-1])
    return result

@csrf_exempt
def getInfo(request):

    info = request.POST['saveContent']
    #開始parse資料
    planList = info.split("|")
    planObject = []
    index = 0
    createTripMain()
    for p in planList:
        if(p!=""):
            detailInfo = p.split("/")
            tmp = TourObject(detailInfo[0].strip(),detailInfo[2].strip(),detailInfo[1].strip())
            createPlan(tmp,index)
            index = index+1
            planObject.append(tmp)
    return render_to_response('test.html', locals())


def index(request):
    return render_to_response('index.html', locals())


def client(request):

    return render_to_response('client.html', locals())



##########################

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

def runServer(request):
    http_server = WSGIServer(('',8009), handler_class=WebSocketHandler)
    http_server.serve_forever()