from flask import Flask, render_template,request
import pandas as pd
from now_place import NOW_PLACE
from covid19 import GEO
import folium

import psycopg2
from dataaccess import DataAccess
from var import Var
from db import DB 
from decimal import Decimal

app = Flask(__name__)

da = DataAccess()
spot_list = da.get_spots()

# @app.route('/')
# def food():
#     # 現在地取得
#     n_place=NOW_PLACE()
#     lat1, lat2, lon1, lon2 = n_place.n_place()

#     # csv
#     tokyo_l = pd.read_csv('data/130001_tokyo_leadermap_ver1.0.csv')
#     tokyo_t = pd.read_csv('data/130001_tokyo_tenpomap_ver1.0.csv')

#     # 東京のコロナ対策リーダー_markers1
#     tokyo_leader = []
#     for name, longitude, latitude in zip(tokyo_l['事業所・店舗名'], tokyo_l['経度'], tokyo_l['緯度']):
#         name = str(name)
#         dic = {'name':name.replace('\r', ''), 'lat':latitude, 'lon':longitude}
#         if dic['lat'] <= lat1 and dic['lat'] >= lat2:
#             if dic['lon'] <= lon1 and dic['lon'] >= lon2:
#                 tokyo_leader.append(dic)
    
#     # 東京の感染防止ステッカー店_markers2
#     tokyo_tenpo = []
#     for name, gyosyu, longitude, latitude in zip(tokyo_t['事業所店舗名'], tokyo_t['業種'], tokyo_t['経度'], tokyo_t['緯度']):
#         name = str(name)
#         dic = {'name':name.replace('\r', ''), 'gyosyu':gyosyu, 'lat':latitude, 'lon':longitude}
#         if dic['lat'] <= lat1 and dic['lat'] >= lat2:
#             if dic['lon'] <= lon1 and dic['lon'] >= lon2:
#                 tokyo_tenpo.append(dic)
#     return render_template('food.html',markers1=tokyo_leader, markers2=tokyo_tenpo)

@app.route('/')
def food():
    # 現在地取得
    n_place=NOW_PLACE()
    lat1, lat2, lon1, lon2 = n_place.n_place()
    
    # 東京のコロナ対策リーダー
    tokyo_leader = []
    spot_list = da.get_spots()
    for spot in spot_list:
        dic = {'name':spot[0], 'lat':float(spot[1]), "lon":float(spot[2])}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                tokyo_leader.append(dic)
                
        # データ確かめ
        # if spot[2] is None:
        #   print(spot[0])
    
    
    tokyo_tenpo = []
    spot_list = da.get_spots1()
    for spot in spot_list:
        dic = {'name':spot[0],'gyousyu':spot[1], 'lat':float(spot[2]), "lon":float(spot[3])}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                tokyo_tenpo.append(dic)
                
        # if spot[2] is None:
        #     print(spot[0])
    
    return render_template('food.html'
                           ,markers1=tokyo_leader
                        ,markers2=tokyo_tenpo
                           )


# @app.route('/medical')
# def medical():
#     # 現在地取得
#     n_place=NOW_PLACE()
#     lat1, lat2, lon1, lon2 = n_place.n_place()

#     # csv
#     kensajo = pd.read_csv('data/kensajo_ver1.0.csv',encoding="shift-jis", header=None)
#     iryokikan = pd.read_csv('data/医療機関_ver1.0.csv')

#     # 東京の検査所_markers3
#     kensajo_2 = []
#     for name, longitude, latitude in zip(kensajo[0], kensajo[5], kensajo[4]):
#         dic = {'name':name.replace('\r', ''),'lat':latitude, 'lon':longitude}
#         if dic['lat'] <= lat1 and dic['lat'] >= lat2:
#             if dic['lon'] <= lon1 and dic['lon'] >= lon2:
#                 kensajo_2.append(dic)

#     # 東京の医療機関_markers4
#     iryokikan_2 = []
#     for name, longitude, latitude in zip(iryokikan['医療機関名'], iryokikan['Unnamed: 40'], iryokikan['Unnamed: 39']):
#         dic = {'name':name.replace('\r', ''),'lat':latitude, 'lon':longitude}
#         if dic['lat'] <= lat1 and dic['lat'] >= lat2:
#             if dic['lon'] <= lon1 and dic['lon'] >= lon2:
#                 iryokikan_2.append(dic)
#     return render_template('medical.html', markers3=kensajo_2, markers4=iryokikan_2)

@app.route('/medical')
def medical():
    # 現在地取得
    n_place=NOW_PLACE()
    lat1, lat2, lon1, lon2 = n_place.n_place()
    kensajo_2 = []
    spot_list = da.get_spots2()
    for spot in spot_list:
        dic = {'name':spot[0], 'lat':float(spot[1]), "lon":float(spot[2])}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                kensajo_2.append(dic)
    
    # # 東京の医療機関_markers4
    iryokikan_2 = []
    spot_list = da.get_spots3()
    for spot in spot_list:
        dic = {'name':spot[0], 'lat':float(spot[1]), "lon":float(spot[2])}
        if dic['lat'] <= lat1 and dic['lat'] >= lat2:
            if dic['lon'] <= lon1 and dic['lon'] >= lon2:
                iryokikan_2.append(dic)

    return render_template('medical.html'
                           , markers3=kensajo_2, markers4=iryokikan_2
                           )

@app.route('/geo')
def polygon_plot():
    g = GEO()
    geometry = g.polygon()

    map = folium.Map(location=[35.68066659206367, 139.7681614127473], zoom_start=14)
    
    max = 0
    for geos in geometry:
        if max < geos[1]:
            max = geos[1]

    for geos in geometry:
        geo = geos[0]
        covid_num = geos[1] / max

        map.choropleth(geo_data=geo, 
                fill_color="red", fill_opacity=0.5 * covid_num, 
                line_color="black", line_opacity=0.3)
    
    filepath = 'templates/covid19.html'
    map.save(filepath)
    return render_template("covid19.html")

# def search(self):
#     if request.method == 'POST':
#         word = request.form['s']
#         query =f"SELECT 事業所・店舗名, 緯度, 経度 FROM leader_map WHERE 事業所・店舗名 LIKE '%ピアトゥー%' "
#         data = ()
#         db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
#         db.execute(query, data)

@app.route('/',methods=['POST', "GET"])
def search_plot():
    
    g = GEO()
    geometry = g.polygon()
    
    map = folium.Map(location=[35.68066659206367, 139.7681614127473], zoom_start=14)
    
    if request.method == 'POST':
        word = request.form['s']
        conn = psycopg2.connect("host=localhost port=5432 dbname=tochiji user=yasu5 password=yuto5715")
        cur = conn.cursor()
        cur.execute(f"SELECT 事業所・店舗名, 緯度, 経度 FROM leader_map WHERE 事業所・店舗名 LIKE '%{word}%' ")
        for row in cur:
            # print(row)
            folium.Marker(
            location =[row[1],row[2]],
            popup =row[0],
            icon = folium.Icon(color='red',icon='home')
        ).add_to(map)
        
        cur.close()
        conn.close()
        
    max = 0
    for geos in geometry:
        if max < geos[1]:
            max = geos[1]

    for geos in geometry:
        geo = geos[0]
        covid_num = geos[1] / max

        map.choropleth(geo_data=geo, 
                fill_color="red", fill_opacity=0.5 * covid_num, 
                line_color="black", line_opacity=0.3)
    
    filepath = 'templates/covid19.html'
    map.save(filepath)
    
    return render_template("covid19.html")
        
        



if __name__ == "__main__":
    app.run(debug = True)
