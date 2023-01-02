from user import User
from misc import *


class OPController:
    def __init__(self):
        self.op_list = {}
        self.exit_key = None

    def show(self):
        print("---------------Menu---------------")
        for op_code, op in self.op_list.items():
            print(f"Key: {op_code} -> {op['text']}")
        print("----------------------------------")

    def match(self, op_code):
        print(f"---------{self.op_list[op_code]['text']}---------")
        self.op_list[op_code]['run']()

    def set_rule(self, dict: Dict):
        self.op_list = dict

    def get_next_op(self):
        self.show()
        op = IOController.get_op_code()
        self.match(str(op))
        return True if str(op) != self.exit_key else False

    def set_exit_key(self, key):
        self.exit_key = key
class UserDict(ObjectHashMap):
    def __init__(self):
        super().__init__(type_name="user", object_type=User)


class CollaborativeSheets:
    def __init__(self):
        self.users = UserDict()
        self.op_controller = OPController()
        self.op_controller.set_exit_key('7')
        self.op_controller.set_rule({
            '1': {'text': "Create a user", 'run': self._create_user},
            '2': {'text': "Create a sheet", 'run': self._create_sheet},
            '3': {'text': "Check a sheet", 'run': self._check_sheet},
            '4': {'text': "Change a value in a sheet", 'run': self._update_value},
            '5': {'text': "Change a sheet's access right", 'run': self._change_sheet_right},
            '6': {'text': "Collaborate with an other user", 'run': self._collaborate_with_other},
            '7': {'text': "exit", 'run': self._exit},
        })


    def run(self):
        end = True
        while end:
            end = self.op_controller.get_next_op()

    def _create_user(self):
        username = IOController.get_username()
        if not self.users.is_exist(username):
            self.users.update(User(username))

    def _get_user_by_input_name(self):
        user_name = IOController.get_username(prefix="target ")
        return self.users.get(user_name)

    def _create_sheet(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = IOController.get_sheet_name(prefix="new sheet ")
            user.create_new_sheet(sheet_name)
        else:
            self.error()

    def _check_sheet(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = IOController.get_sheet_name(prefix="new sheet name/")
            user.show_sheet(sheet_name)
        else:
            self.error()

    def _update_value(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = input(f"target sheet {user.name}/")
            user.open_edit_mode(sheet_name)

    def _change_sheet_right(self):
        user = self._get_user_by_input_name()
        if user:
            sheet_name = IOController.get_sheet_name(prefix="target ")
            user.update_sheet_access_right(sheet_name, AccessRight.read_only)
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
            print("commend failed")

    def _exit(self):
        print("application end")

    def error(self):
        print("Sorry, command failed, please try again")


def main():
    app = CollaborativeSheets()
    app.run()


if __name__ == "__main__":
    main()
