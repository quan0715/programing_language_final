import pandas as pd

from misc import *


class Sheet:
    ROW_NUMBER = 3
    COLUMN_NUMBER = 3

    def __init__(self, name):
        self.name = name
        self.sheet = [[0 for _ in range(Sheet.COLUMN_NUMBER)] for __ in range(Sheet.COLUMN_NUMBER)]
        self.access_right = AccessRight.editable
        print(f'sheet: "{self.name}" creat successfully')

    def change_access_right(self, access_right: AccessRight):
        self.access_right = access_right
        print(f'sheet: {self.name} access right: {access_right}')

    def edit_mode(self):
        if self.access_right == AccessRight.read_only:
            print("This sheet is not accessible.")
            return None
        EditMode.open(self)

    def __repr__(self):
        df = pd.DataFrame(self.sheet)
        return df.to_markdown()


class EditMode:
    # singleton object
    def __init__(self):
        self._id = id(self)

    def get_id(self):
        return self._id

    @classmethod
    def open(cls, target_sheet: Sheet):
        print("-----------------Edit Mode------------------")
        while True:
            user_input = IOController.get_sheet_edit_command()
            if not user_input:
                print("---------------End Edit Mode---------------")
                print(target_sheet)
                break
            elif user_input == "invalid input":
                print("invalid input")
                continue
            else:
                row_idx, col_idx, value = user_input
                try:
                    target_sheet.sheet[row_idx][col_idx] = value
                except IndexError:
                    print(f"row_idx {row_idx} or col_idx {col_idx} are out of range")
                print(target_sheet)
