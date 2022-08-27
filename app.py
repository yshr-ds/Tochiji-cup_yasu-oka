from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')

def root():
    markers=[
    {
    'lat':35.68066659206367,
    'lon':139.7681614127473,
    'popup':'This is sample website of the Tochiji cup.'
        }
    ]
    tokyo_l = pd.read_csv('data/130001_tokyo_leadermap_ver1.0.csv')
    tokyo_t = pd.read_csv('data/130001_tokyo_tenpomap_ver1.0.csv')
    kensajo = pd.read_csv('data/kensajo_ver1.0.csv',encoding="shift-jis", header=None)
    iryokikan = pd.read_csv('data/医療機関_ver1.0.csv')

    # 東京のコロナ対策リーダー_markers1
    tokyo_leader = []
    for name, longitude, latitude in zip(tokyo_l['事業所・店舗名'], tokyo_l['経度'], tokyo_l['緯度']):
        dic = {'name':name, 'lat':latitude, 'lon':longitude}
        tokyo_leader.append(dic)
    
    # 東京の感染防止ステッカー店_markers2
    tokyo_tenpo = []
    for name, gyosyu, longitude, latitude in zip(tokyo_t['事業所店舗名'], tokyo_t['業種'], tokyo_t['経度'], tokyo_t['緯度']):
        dic = {'name':name, 'gyosyu':gyosyu, 'lat':latitude, 'lon':longitude}
        tokyo_tenpo.append(dic)

    # 東京の検査所_markers3
    kensajo_2 = []
    for name, longitude, latitude in zip(kensajo[0], kensajo[5], kensajo[4]):
        dic = {'name':name,'lat':latitude, 'lon':longitude}
        kensajo_2.append(dic)

    # 東京の医療機関_markers4
    iryokikan_2 = []
    for name, longitude, latitude in zip(iryokikan['医療機関名'], iryokikan['Unnamed: 40'], iryokikan['Unnamed: 39']):
        dic = {'name':name,'lat':latitude, 'lon':longitude}
        iryokikan_2.append(dic)

    return render_template('index.html',markers1=tokyo_leader, markers2=tokyo_tenpo, markers3=kensajo_2, markers4=iryokikan_2 )

if __name__ == "__main__":
    app.run(debug = True)
