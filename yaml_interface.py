import yaml


class YamlInterface:

    def __init__(self):
        self.paths = {
            'stations': './Market/static_data/sde/bsd/staStations.yaml'
        }

    def query(self, file_name, fields):
        path = self.paths[file_name]
        file = self.open(path)

        query_result = []
        for item in file:

            item_result = {}
            for field in fields:
                try:
                    item_result[field] = item[field]
                except ValueError as e:
                    print('Invalid field for query')
                    return False

            query_result.append(item_result)

        return query_result

    @staticmethod
    def open(self, path):
        with open(path) as file:
            return yaml.load(file, Loader=yaml.FullLoader)
