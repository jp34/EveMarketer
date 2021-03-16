from openpyxl import load_workbook


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

    def read(self, columns, rows):
        try:
            file_contents = []
            for row in rows:
                row_string = str(row)

                row_list = []
                for column in columns:
                    row_list.append(self.sheet[str(column + row_string)])

                file_contents.append(row_list)

            return file_contents

        except Exception as e:
            print('Invalid arguments for reading:', e)
            return False

    def read_columns(self, columns):
        pass
