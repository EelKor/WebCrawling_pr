#날씨 크롤링 프로그램
#   
#   *네이버 날씨에서 데이터 추출
#   *파이썬3.7
#   *결과값인 날씨 데이터는 2차원리스트 형식으로 출력
#   *향후 무인기 프로젝트시 바람방향, 풍속등 데이터 실시간으로 전송 가능
#
#   = Weather(결과값) = [[요일, 오전강수확률%, 오후강수확률%, 최고기온, 최저기온], [요일, ........]
#
#  ****************************
#   *작  성  자 : 이승신
#   *작  성  일 : 2020-08-29
#   *인터프리터 : python3.7
#
#******************************

#모듈 임포트##################
from bs4 import BeautifulSoup
from pprint import pprint
import requests


##############################
#디버그 모드 설정
DEBUG = True

###############################
if DEBUG:
    import time
    startTime = time.time()

#웹페이지 불러오기
html = requests.get("https://search.naver.com/search.naver?query=날씨")
#웹페이지 파싱
soup = BeautifulSoup(html.text, 'html.parser')

#파싱작업 끝난 데이터 필요한 부분만 추출
data_weather1 = soup.find('div' , {'class':'weather_box'})

#data_weather1정보중 현재 주소 추출
find_address = data_weather1.find('span',{'class':'btn_select'}).text
print("현재위치:"+find_address)

#data_weather1 정보중 현재 온도 추출
find_temperture = data_weather1.find('span',{'class':'todaytemp'}).text
print("현재온도:"+find_temperture +"*C")

#미세먼지 값 추출
data2 = data_weather1.findAll('dd')

fine_dust = data2[0].find('span', class_='num').text
print("미세먼지:" +fine_dust)

ufine_dust = data2[1].find('span',class_='num').text
print("초미세먼지:" +ufine_dust)


#주간 날씨 불러오기
data_weeklyWeather1 = soup.find('div', class_='table_info weekly _weeklyWeather') 
data_weeklyWeather1 =data_weeklyWeather1.find('ul')
list_weeklyWeather1 = data_weeklyWeather1.findAll('li')

#주간 날씨 리스트 자료형 선언
#***************************
# <feedback>
#원래 딕셔너리 자료형 을 사용했으나
#딕셔너리 value 값에 순서가 없음을 간과함
#list 자료형 사용

Weather = []
index = 1
for _week in list_weeklyWeather1:
    Head_week = _week.find('span', class_="day_info").text
    Head_week = Head_week[:1]
    
    #네이버 웹 형식상 오늘날짜 html 코드와 다른 날짜의 html코드가 다름,
    #오늘 오전 강수확률은 class = "rain_rate wet" 이나 오늘이 아닌 날은 모두 rain_rate 만 사용
    #따라 오늘날짜 일때만( 첫실행 ) 따로 처리하도록 작성
    if index == 1:
        value_MorningRainrate = _week.find('span', class_="point_time morning")
        value_MorningRainrate = value_MorningRainrate.find('span', class_="rain_rate wet")
        value_MorningRainrate = value_MorningRainrate.find('span', class_="num").text + '%'
    
    else:
        value_MorningRainrate = _week.find('span', class_="point_time morning")
        value_MorningRainrate = value_MorningRainrate.find('span', class_="rain_rate")
        value_MorningRainrate = value_MorningRainrate.find('span', class_="num").text + "%"

    #오후 강수확률
    value_AfternoonRainrate = _week.find('span', class_="point_time afternoon")
    value_AfternoonRainrate = value_AfternoonRainrate.find('span', class_="rain_rate")
    value_AfternoonRainrate = value_AfternoonRainrate.find('span', class_="num").text + "%"

    #최고기온 최저기온 추출
    value_TempHigh = _week.find('dl')
    value_TempHigh = value_TempHigh.find('dd')
    value_TempHigh = value_TempHigh.findAll('span')
    value_TempLow = value_TempHigh[0].text
    value_TempHigh = value_TempHigh[2].text

    #최종 결과값인 Weather 리스트 에 전달하기 전 데이터 패키징(리스트형식)
    temp = []
    temp.append(Head_week)
    temp.append(value_MorningRainrate)
    temp.append(value_AfternoonRainrate)
    temp.append(value_TempHigh)
    temp.append(value_TempLow)

    #결과값 전달 Weather로 
    Weather.append(temp)

    #반복문 디버깅 코드 (실행횟수 표시)
    if DEBUG:
        print("반복문",index,"회 실행")

    index += 1

#테스트출력
if DEBUG:
    end = time.time() - startTime
    print("코드 실행시간 :", end, "s")
print(Weather)