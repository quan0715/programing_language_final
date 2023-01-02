from enum import Enum
from typing import Dict


class AccessRight(Enum):
    read_only = "readonly"
    editable = "editable"


class IOController:
    def __init__(self):
        self._id = id(self)

    @classmethod
    def get_username(cls, prefix=""):
        return input(f"{prefix}username > ")

    @classmethod
    def get_op_code(cls):
        while True:
            try:
                op = int(input("> "))
                if 1 <= op <= 7:
                    break
                print("input out of range, please input number 1 ~ 7")
            except ValueError:
                print('invalid input, please input number 1 ~ 7')
        return op

    @classmethod
    def get_sheet_name(cls, prefix=""):
        return input(f"{prefix}sheet name > ")

    @classmethod
    def get_sheet_edit_command(cls):
        print("input format <row_idx> <col_idx> <value or operation>")
        print("type q or quit to end edit mode")
        user_input = input("> ")
        if user_input.lower() == "q" or user_input.lower() == "quit":
            return False
        else:
            user_input = user_input.split(' ')
            try:
                return int(user_input[0]), int(user_input[1]), eval(user_input[2])

            except:
                return "invalid input"

    @classmethod
    def get_access_right(cls):
        access_right = input(f'(R/r: readonly, E/e:editable) > ')
        if access_right.lower()[0] == 'r':
            return AccessRight.read_only
        elif access_right.lower()[0] == 'e':
            return AccessRight.editable
        else:
            print("invalid access right, try ReadOnly and Editable")
            return False


class ObjectHashMap:
    def __init__(self, type_name, object_type):
        self.type_name = type_name
        self.object_type = object_type
        self.dict: Dict[str, f'object_type'] = {}

    def get(self, key):
        try:
            return self.dict[key]
        except KeyError:
            return self.key_error(key)

    def update(self, target_object):
        self.dict[target_object.name] = target_object

    def key_error(self, key):
        create = input(
            f'{self.type_name} "{key}" does not exist, do you want to create new {self.type_name} with name {key}? (y/n) > '
        )
        if create.lower() == 'y':
            new_o = self.object_type(key)
            self.update(new_o)
            return new_o
        else:
            keys = tuple(self.dict.keys())
            print(f"you can try existing {self.type_name} name \n > {keys}")

    def is_exist(self, key) -> bool:
        flag = key in self.dict.keys()
        if flag:
            print(f"sorry {self.type_name} \"{key}\" has already been created, please try another name")
        return flag
