from openpyxl import load_workbook
import mysql.connector
import os

base_path = 'Market/data/sde/fsd/universe/eve'


def get_region_path(region):
    return base_path + '/' + region


def get_const_path(region, const):
    return get_region_path(region) + '/' + const


# Get data from folder directories
constellation_dict = {} # {Constellation : Region}
system_dict = {}        # {System : (Region, Const)}

regions = [f.name for f in os.scandir(base_path) if f.is_dir()]

# Create tree of location names
# Iterate over region folders
for region in regions:
    region = region.replace(" ", "")

    # Iterate over constellation sub folders
    path = get_region_path(region)
    constellations = [f.name for f in os.scandir(path) if f.is_dir()]
    for const in constellations:
        const = const.replace(" ", "")
        constellation_dict[const] = region

        # Iterate over system sub folders
        path = get_const_path(region, const)
        systems = [f.name for f in os.scandir(path) if f.is_dir()]
        for system in systems:
            system = system.replace(" ", "")
            system_dict[system] = (region, const)


class ExcelInterface:

    def __init__(self, book_path, sheet_name):
        # Import excel file
        self.book = load_workbook(filename=book_path)
        self.sheet = self.book[sheet_name]

    def read_row(self, columns, row):
        row_result = []
        for column in columns:
            row_result.append(self.sheet[column + str(row)].value)
        if len(row_result) == 0:
            return False
        else:
            return row_result


# Get data from excel
excel_path = 'Market/data/excel_docs/EveLocationData.xlsx'

region_ids = {}     # region_id : region_name
constell_ids = {}   # constell_id : constell_name
system_ids = {}     # system_id : system_name

sheet_names = ['region_ids', 'constell_ids', 'system_ids']
dicts = [region_ids, constell_ids, system_ids]

for i in range(0, 3):
    interface = ExcelInterface(excel_path, sheet_names[i])

    end = False
    row = 1
    while not end:
        data = interface.read_row(['A', 'B'], row)
        if data[0] == None:
            end = True
        else:
            id = data[0]
            name = data[1].replace(" ", "")

            dict = dicts[i]
            dict[id] = name

        row += 1

# DB regions (region_id, region_name)
# DB constellations (constell_id, constell_name, region_id, region_name)
# DB systems (system_id, system_name, region_id, reigon_name, constell_id, constell_name)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Football34",
    database='eve_market_db'
)

cursor = connection.cursor()

system_not_found = []
constell_not_found = []

could_not_read = []

region_keys = list(region_ids.keys())
region_values = list(region_ids.values())

constell_keys = list(constell_ids.keys())
constell_values = list(constell_ids.values())

# Combine data
for data in system_ids:

    # Get system info
    system_id = data
    system_name = system_ids[data]

    # Get region_name and constell_name
    try:
        data = system_dict[system_name]
    except KeyError as e:
        system_not_found.append(system_name)
        continue

    try:
        region_name = data[0]
        constell_name = data[1]
    except TypeError as e:
        could_not_read.append(data)
        continue

    index = region_values.index(region_name)
    region_id = region_keys[index]

    try:
        index = constell_values.index(constell_name)
        constell_id = constell_keys[index]
    except ValueError as e:
        constell_not_found.append(constell_name)

    sql = f'INSERT INTO systems (system_id, system_name, region_id, region_name, con_id, con_name) VALUES (%s, %s, %s, %s, %s, %s)'
    values = (system_id, system_name, region_id, region_name, constell_id, constell_name)

    cursor.execute(sql, values)
    connection.commit()
