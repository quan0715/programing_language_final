from user import User
from misc import *


class OPController:
    op_list = {}

    def __init__(self):
        self.id = id(self)

    @classmethod
    def show(cls):
        IOController.print_mode_head('MENU')
        for op_code, op in cls.op_list.items():
            print(f"Key: {op_code} -> {op['text']}")
        IOController.print_mode_bottom()

    @classmethod
    def match(cls, op_code):
        IOController.print_mode_head(cls.op_list[op_code]['text'].upper())
        cls.op_list[op_code]['run']()
        IOController.print_mode_bottom()

    @classmethod
    def set_rule(cls, d: Dict):
        cls.op_list = d


class UserDict(ObjectHashMap):
    def __init__(self):
        super().__init__(type_name="user", object_type=User)


class CollaborativeSheets:
    def __init__(self):
        self.users = UserDict()
        OPController.set_rule({
            '1': {'text': "Create a user", 'run': self._create_user},
            '2': {'text': "Create a sheet", 'run': self._create_sheet},
            '3': {'text': "Check a sheet", 'run': self._check_sheet},
            '4': {'text': "Change a value in a sheet", 'run': self._update_value},
            '5': {'text': "Change a sheet's access right", 'run': self._change_sheet_right},
            '6': {'text': "Collaborate with an other user", 'run': self._collaborate_with_other},
            '7': {'text': "exit", 'run': self._exit},
        })

    def run(self):
        op = 1
        while op != 7:
            OPController.show()
            op = IOController.get_op_code()
            OPController.match(str(op))

    def _create_user(self):
        username = IOController.get_username()
        if not self.users.is_exist(username):
            self.users.update(User(username))
            IOController.print_created_success_message("user", username)

    def _get_user_by_input_name(self):
        user_name = IOController.get_username(prefix="target ")
        return self.users.get(user_name)

    def _create_sheet(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = IOController.get_sheet_name(prefix="new ")
            user.create_new_sheet(sheet_name)
        else:
            self.error()

    def _check_sheet(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = IOController.get_sheet_name(prefix="target ")
            user.show_sheet(sheet_name)
        else:
            self.error()

    def _update_value(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = IOController.get_sheet_name(prefix="target ")
            user.open_edit_mode(sheet_name)

    def _change_sheet_right(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = IOController.get_sheet_name(prefix="target ")
            user.update_sheet_access_right(sheet_name)
        else:
            self.error()

    def _collaborate_with_other(self):
        host_user_name = IOController.get_username(prefix="host ")
        host = self.users.get(host_user_name)
        if host:
            shared_sheet_name = IOController.get_sheet_name(prefix="Shared ")
            collaborator_name = IOController.get_username(prefix="collaborator ")
            collaborator = self.users.get(collaborator_name)
            if collaborator:
                host.collaborate_on_other_sheet(shared_sheet_name, collaborator)
        else:
            self.error()

    def _exit(self):
        print("application end")

    def error(self):
        print("Sorry, command failed or the operation is not allowed, please try again")


def main():
    app = CollaborativeSheets()
    app.run()


if __name__ == "__main__":
    main()
