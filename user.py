from sheet import Sheet
from misc import *


class SheetDict(ObjectHashMap):
    def __init__(self):
        super().__init__(type_name="sheet", object_type=Sheet)


class User:
    def __init__(self, name):
        self.name = name
        self.sheets = SheetDict()

    def create_new_sheet(self, sheet_name: str):
        if not self.sheets.is_exist(sheet_name):
            self.sheets.update(Sheet(sheet_name))
            IOController.print_created_success_message("sheet", sheet_name)
            return self.sheets.get(sheet_name)

    def show_sheet(self, sheet_name: str):
        target_sheet = self.sheets.get(sheet_name)
        if target_sheet:
            print(target_sheet)

    def update_sheet(self, sheet_name: str, row_idx: int, col_idx: int, value: int):
        target_sheet = self.sheets.get(sheet_name)
        if target_sheet:
            target_sheet.update_value(row_idx, col_idx, value)

    def open_edit_mode(self, sheet_name: str):
        target_sheet = self.sheets.get(sheet_name)
        if target_sheet:
            target_sheet.edit_mode()

    def update_sheet_access_right(self, sheet_name: str):
        target_sheet = self.sheets.get(sheet_name)
        if target_sheet:
            access_right = IOController.get_access_right()
            if access_right:
                target_sheet.change_access_right(access_right)

    def collaborate_on_other_sheet(self, target_sheet_name: str, collaborator: 'User'):
        target_sheet = self.sheets.get(target_sheet_name)
        if target_sheet:
            collaborator.sheets.update(target_sheet)
            print(f'Share "{self.name}"\'s "{target_sheet_name}" with "{collaborator.name}".')
        else:
            print("command failed")