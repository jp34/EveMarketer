import requests


class MarketApi:

    def __init__(self):
        # URL Data
        self.data_url = 'https://esi.evetech.net/latest'


    # Market price data
    def get_market_prices(self):
        return self.pull_data("/markets/prices/?datasource=tranquility")


    def get_historical_data(self, region_id, type_id):
        return self.pull_data(f"/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}")


    # Order data
    def get_character_orders(self, character_id):
        return self.pull_data(f"/characters/{character_id}/orders/?datasource=tranquility")


    def get_character_history(self, character_id):
        return self.pull_data(f"/markets/groups/{character_id}/?datasource=tranquility&language=en-us")


    def get_corp_orders(self, corporation_id):
        return self.pull_data(f"/corporations/{corporation_id}/orders/?datasource=tranquility")


    def get_corp_history(self, corporation_id):
        return self.pull_data(f"/corporations/{corporation_id}/orders/history/?datasource=tranquility")


    def get_region_orders(self, region_id, order_type=all):
        return self.pull_data(f"/markets/{region_id}/orders/?datasource=tranquility&order_type={order_type}")


    def get_structure_orders(self, structure_id):
        return self.pull_data(f"/markets/structures/{structure_id}/?datasource=tranquility")


    # Item data
    def get_item_groups(self):
        return self.pull_data("/markets/groups/?datasource=tranquility")


    def get_item_info(self, market_group_id):
        return self.pull_data(f"/markets/groups/{market_group_id}/?datasource=tranquility&language=en-us")


    # Get character data


    # Pull data from esi
    def pull_data(self, data_path):
        try:
            url = self.data_url + data_path
            data = requests.get(url).content.decode('utf_8')
            data_list = eval(data)
            return data_list
        except Exception as e:
            print("[ERROR] Cannot get data:", e)
            return False
