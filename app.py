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
    # geometry = g.polygon()
    df, date, poly = g.polygon()

    map = folium.Map(location=[35.68066659206367, 139.7681614127473], zoom_start=14)

    poly = poly
    data = df
    bins = list(df['陽性者割合'].quantile([0, 0.25, 0.5, 0.75, 1]))
    folium.Choropleth(
        geo_data=poly,
        name='choropleth',
        data=data,
        columns=['市区町村名','陽性者割合'],
        key_on='properties.N03_004',
        fill_color="RdPu", 
        fill_opacity=0.5, 
        line_color="black", 
        line_opacity=0.3, 
        legend_name=f"[{date}] 市区町村ごとのコロナ陽性者の指標",
        bins=bins,
        reset=True,
        ).add_to(map)

    folium.LayerControl().add_to(map)

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
    df, date, poly = g.polygon()
    
    map = folium.Map(location=[35.68066659206367, 139.7681614127473], zoom_start=14)
    
    if request.method == 'POST' and request.form.get('s'):
        word = request.form['s']
        conn = psycopg2.connect(f"host={Var.hostname} port={Var.port} dbname={Var.dbname} user={Var.username} password={Var.password}")
        cur = conn.cursor()
        cur.execute(f"SELECT 事業所・店舗名, 緯度, 経度 FROM leader_map WHERE 事業所・店舗名 LIKE '%{word}%' ")
        for row in cur:
            folium.Marker(
            location =[row[1],row[2]],
            popup =row[0],
            icon = folium.Icon(color='red',icon='home')
        ).add_to(map)

        cur.close()
        conn.close()

    if request.method == 'POST' and request.form.get('n'):
        word = request.form['n']
        conn = psycopg2.connect(f"host={Var.hostname} port={Var.port} dbname={Var.dbname} user={Var.username} password={Var.password}")
        cur = conn.cursor()
        cur.execute(f"SELECT 事業所店舗名, 業種, 緯度, 経度 FROM tenpo_map WHERE 業種 LIKE '%{word}%' ")
        for row in cur:
            folium.Marker(
            location =[row[2],row[3]],
            popup =row[1],
            icon = folium.Icon(color='red',icon='home')
        ).add_to(map)

        cur.close()
        conn.close()


    poly = poly
    data = df
    bins = list(df['陽性者割合'].quantile([0, 0.25, 0.5, 0.75, 1]))
    folium.Choropleth(
        geo_data=poly,
        name='choropleth',
        data=data,
        columns=['市区町村名','陽性者割合'],
        key_on='properties.N03_004',
        fill_color="RdPu", 
        fill_opacity=0.5, 
        line_color="black", 
        line_opacity=0.3, 
        legend_name=f"[{date}] 市区町村ごとのコロナ陽性者の指標",
        bins=bins,
        reset=True,
        ).add_to(map)
    folium.LayerControl().add_to(map)

    
    filepath = 'templates/covid19.html'
    map.save(filepath)
    
    return render_template("covid19.html")
        
        



if __name__ == "__main__":
    app.run(debug = True)
