# This is a sample Python script.
# noinspection PyUnresolvedReferences
import auth as slnet
import get_user_id
import get_user_info
import starlineapi as sl


from get_app_code import get_app_code
from get_app_token import get_app_token
from get_slid_user_token import get_slid_user_token
from get_slnet_token import get_slnet_token


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():

    slid_token = "ef9d7318df61dba1b824ec36bb220ddc:1045837"
    user = sl.get_user_id(slid_token)
    slnet_token = sl.get_slnet_token(slid_token)
    user_info = sl.get_user_info(user, slnet_token)
    if user_info.get('codestring') == 'OK':
        for devices in iter(user_info['devices']):
            print(devices)
        for shared_devices in iter(user_info['shared_devices']):
            print(shared_devices)
    else:
        print('data url error')


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
