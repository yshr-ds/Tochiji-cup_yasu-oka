from dataaccess import DataAccess
import pandas as pd
import os

da = DataAccess()

query = 'DROP TABLE IF EXISTS sightseeing_ai_tech; \
\
CREATE TABLE sightseeing_ai_tech (\
    spot_id SERIAL PRIMARY KEY,\
    spot_area TEXT,\
    spot_name TEXT,\
    spot_latitude TEXT,\
    spot_longitude TEXT,\
    spot_opentime INTEGER,\
    spot_closetime INTEGER,\
    category_see INTEGER,\
    category_play INTEGER,\
    category_eat INTEGER,\
    category_buy INTEGER,\
    season_spring INTEGER,\
    season_summer INTEGER,\
    season_autumn INTEGER,\
    season_winter INTEGER\
);'

if __name__ == "__main__":
    da.create_table(query)
    basedir = os.path.dirname(__file__)

    query = "INSERT INTO sightseeing_ai_tech (spot_area, spot_name, spot_latitude, spot_longitude, spot_opentime, spot_closetime, category_see, category_play, category_eat, category_buy, season_spring, season_summer, season_autumn, season_winter)\
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    # エラーの場合は絶対パスで指定
    df = pd.read_csv(basedir + '/spot_list.csv')
    data_list = []
    for i in df.values:
        data_list.append(list(i))
    for data in data_list:
        da.insert_data(query, data)

    query = "ALTER TABLE sightseeing_ai_tech ALTER COLUMN spot_opentime TYPE TIME USING CAST(CAST((spot_opentime / 100) AS TEXT) || ':00' AS TIME);\
            ALTER TABLE sightseeing_ai_tech ALTER COLUMN spot_closetime TYPE TIME USING CAST(CAST((spot_closetime / 100) AS TEXT) || ':00' AS TIME);"
    da.create_table(query)