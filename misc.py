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
                print("invalid input")
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

    @classmethod
    def repeated_name_found(cls, type_name, key):
        print(f"sorry {type_name} \"{key}\" has already been created, please try another name")

    @classmethod
    def ask_for_create_instance(cls, type_name, key):
        create_or_not = input(
            f'{type_name} "{key}" does not exist, do you want to create new {type_name} with name {key}? (y/n) > '
        )
        return create_or_not.lower()

    @classmethod
    def print_existing_instance(cls, type_name, d: dict):
        print(f"you can try existing {type_name} name \n > {d.keys()}")

    @classmethod
    def print_mode_head(cls, mode_name):
        print(f'{str(mode_name).center(40,"-")}')
        pass

    @classmethod
    def print_mode_bottom(cls):
        print(f'{"-"*40}')
        pass

    @classmethod
    def print_created_success_message(cls, type_name, key):
        print(f'{type_name}: "{key}" creat successfully')

class ObjectHashMap:
    def __init__(self, type_name, object_type):
        self.type_name = type_name
        self.object_type = object_type
        self.dictionary: Dict[str, f'object_type'] = {}

    def get(self, key):
        try:
            return self.dictionary[key]
        except KeyError:
            return self.key_error(key)

    def update(self, target_object):
        self.dictionary[target_object.name] = target_object

    def key_error(self, key):
        creat_or_not = IOController.ask_for_create_instance(self.type_name, key)
        if creat_or_not.lower() == 'y':
            new_o = self.object_type(key)
            self.update(new_o)
            return new_o
        else:
            IOController.print_existing_instance(self.type_name, self.dictionary)

    def is_exist(self, key) -> bool:
        flag = key in self.dictionary.keys()
        if flag:
            IOController.repeated_name_found(self.type_name, key)
        return flag
