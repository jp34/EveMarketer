import json


class JSONManager:


    def __init__(self):
        self.json_folder = "./api/server/data/json/"


    def get_data(self, file, parameter):
        """
        Input:
            - file : JSON file name to look for search parameter
            - parameter : Search parameter for json file
        Output:
            - Returns data found in json file
        """
        data_dict = self.read_json(file)
        return data_dict[parameter]


    def update_json(self, file_name, parameter, new_value):
        """
        Receives
        """
        file_path = str(self.json_folder + file_name + ".json")
        print(file_path)

        json_file = open(file_path, 'r')
        data = json.load(json_file)
        json_file.close()
        
        data[parameter] = new_value

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)


    def read_json(self, file):
        """
        Receives name of json file to be read. Returns python dictionary of found data

        Input:
            - file : name of file to be searched
        Output:
            - data : dictionary containing data from json file
        """
        with open(str(self.json_folder + file + ".json"), 'r') as json_file:
            data = json.load(json_file)
            return data
    

    def write_json(self, file, data):
        """
        Receives python dictionary to be written to json file. Returns nothing

        Inpiut:
            - file : Name of json file to write data to
            - data : Dictionary object to be written to given file
        Output: None
        """
        with open(str(self.json_folder + file + ".json"), 'w') as json_file:
            json.dump(data, json_file, indent=2)
