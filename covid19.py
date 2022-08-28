import pandas as pd
import geopandas as gpd
import datetime

class GEO:
    def polygon(self):
        shapefile_path = 'data/N03-19_13_190101.geojson'
        df = gpd.read_file(shapefile_path, encoding='cp932')
        islands = ['所属未定地','大島町', '利島村', '新島村', '神津島村', '三宅村', '御蔵島村', '八丈町', '青ヶ島村', '小笠原村']
        is_not_islands = [df["N03_004"] != island for island in islands]
        is_not_islands = pd.concat(is_not_islands, axis=1).all(axis=1)
        df = df.loc[is_not_islands, :]
        df = df.drop(['N03_001', 'N03_002', 'N03_003', 'N03_007'], axis=1)
        df = df.rename(columns={'N03_004': '市区町村名'})

        cov = pd.read_csv('data/東京都市区町村別コロナ陽性者数.csv')
        cov = cov[['市区町村名','公表_年月日','陽性者数']]
        cov = cov.dropna()
        cov['公表_年月日'] = pd.to_datetime(cov['公表_年月日'])

        #現在の日付
        # dt_now = datetime.date.today()
        # cov_now = cov[cov['公表_年月日'] == dt_now]
        date_rei = '2022-08-23'
        cov_now = cov[cov['公表_年月日'] == date_rei]

        df_new = pd.merge(df, cov_now, on='市区町村名')

        # 市区町村の人数
        nin = pd.read_csv('data/tn20qv020300.csv', encoding='shift-jis', header=10)
        nin = nin[['地域', '令和2年10月1日(国勢調査) Oct. 1, 2020 (Census)']]
        nin = nin.rename(columns={'地域': '市区町村名', '令和2年10月1日(国勢調査) Oct. 1, 2020 (Census)':'人口'})

        # 結合
        df_new2 = pd.merge(df_new, nin, on='市区町村名')
        df_new2 = df_new2.astype({'人口': int})
        df_new2['陽性者割合'] = df_new2['陽性者数'] / df_new2['人口']

        poly = 'data/N03-19_13_190101.geojson'
        df_n = df_new2[['市区町村名','陽性者割合']]
        date = date_rei
        return df_n, date, poly