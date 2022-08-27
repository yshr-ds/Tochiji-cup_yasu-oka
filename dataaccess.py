from var import Var
from db import DB 

class DataAccess:

    def get_spots(self):
        query = "SELECT 事業所・店舗名, 緯度, 経度 FROM leader_map "
        data = ()
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)
    
    def get_spots1(self):
        query = "SELECT 事業所店舗名, 業種, 緯度, 経度 FROM tenpo_map "
        data = ()
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)
    
    def get_spots2(self):
        query = "SELECT 事業所名, 緯度, 経度 FROM PCR "
        data = ()
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)
    
    def get_spots3(self):
        query = "SELECT 医療機関名, 緯度, 経度 FROM iryoukikan "
        data = ()
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)

    # def get_spots_by_area(self, spot_area):
    #     query = "SELECT * FROM data_spot WHERE spot_area = %s "
    #     data = (str(spot_area), )
    #     db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
    #     return db.execute(query, data)

    # def get_latlng_by_spot_name(self, spot_name):
    #     query = "SELECT spot_latitude, spot_longitude FROM data_spot WHERE spot_name = %s "
    #     data = (str(spot_name), )
    #     db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
    #     return db.execute(query, data)

    # def get_openclose_by_spot_name(self, spot_name):
    #     query = "SELECT spot_opentime, spot_closetime FROM data_spot WHERE spot_name = %s "
    #     data = (str(spot_name), )
    #     db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
    #     return db.execute(query, data)

    # def get_spot_by_features(self, feat1, feat2, feat3, feat4, feat5):
    #     query = "SELECT * FROM data_spot WHERE spot_history_culture = %s AND spot_food_product = %s AND spot_nature = %s AND spot_view = %s AND spot_experience = %s "
    #     data = (str(feat1), str(feat2), str(feat3), str(feat4), str(feat5), )
    #     db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
    #     return db.execute(query, data)

    # def get_spot_by_branch(self, branch):
    #     query = "SELECT * FROM data_spot WHERE spot_opentime < %s AND spot_closetime > %s "
    #     data = (str(branch), str(branch), )
    #     db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
    #     return db.execute(query, data)
