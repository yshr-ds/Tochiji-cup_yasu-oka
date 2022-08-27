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
        cov_now = cov[cov['公表_年月日'] == '2022-08-23']

        df_new = pd.merge(df, cov_now, on='市区町村名')

        geometry = []
        for geo in zip(df_new['geometry'], df_new['陽性者数']):
            geometry.append(geo)
        return geometry