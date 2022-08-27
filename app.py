from flask import Flask, render_template,request
import pandas as pd
from now_place import NOW_PLACE

app = Flask(__name__)


@app.route('/')
def food():
    # 現在地取得
    n_place=NOW_PLACE()
    lat1, lat2, lon1, lon2 = n_place.n_place()

    # csv
    tokyo_l = pd.read_csv('data/130001_tokyo_leadermap_ver1.0.csv')
    tokyo_t = pd.read_csv('data/130001_tokyo_tenpomap_ver1.0.csv')

    # 東京のコロナ対策リーダー_markers1
    tokyo_leader = []
    for name, longitude, latitude in zip(tokyo_l['事業所・店舗名'], tokyo_l['経度'], tokyo_l['緯度']):
        name = str(name)
        dic = {'name':name.replace('\r', ''), 'lat':latitude, 'lon':longitude}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                tokyo_leader.append(dic)
    
    # 東京の感染防止ステッカー店_markers2
    tokyo_tenpo = []
    for name, gyosyu, longitude, latitude in zip(tokyo_t['事業所店舗名'], tokyo_t['業種'], tokyo_t['経度'], tokyo_t['緯度']):
        name = str(name)
        dic = {'name':name.replace('\r', ''), 'gyosyu':gyosyu, 'lat':latitude, 'lon':longitude}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                tokyo_tenpo.append(dic)
    return render_template('food.html',markers1=tokyo_leader, markers2=tokyo_tenpo)


@app.route('/medical')
def medical():
    # 現在地取得
    n_place=NOW_PLACE()
    lat1, lat2, lon1, lon2 = n_place.n_place()

    # csv
    kensajo = pd.read_csv('data/kensajo_ver1.0.csv',encoding="shift-jis", header=None)
    iryokikan = pd.read_csv('data/医療機関_ver1.0.csv')

    # 東京の検査所_markers3
    kensajo_2 = []
    for name, longitude, latitude in zip(kensajo[0], kensajo[5], kensajo[4]):
        dic = {'name':name.replace('\r', ''),'lat':latitude, 'lon':longitude}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                kensajo_2.append(dic)

    # 東京の医療機関_markers4
    iryokikan_2 = []
    for name, longitude, latitude in zip(iryokikan['医療機関名'], iryokikan['Unnamed: 40'], iryokikan['Unnamed: 39']):
        dic = {'name':name.replace('\r', ''),'lat':latitude, 'lon':longitude}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                iryokikan_2.append(dic)
    return render_template('medical.html', markers3=kensajo_2, markers4=iryokikan_2)

if __name__ == "__main__":
    app.run(debug = True)
