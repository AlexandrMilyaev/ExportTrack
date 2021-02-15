# This is a sample Python script.
# noinspection PyUnresolvedReferences
import auth as slnet
import get_user_id
import get_user_info

from get_app_code import get_app_code
from get_app_token import get_app_token
from get_slid_user_token import get_slid_user_token
from get_slnet_token import get_slnet_token


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():

    slid_token = "ef9d7318df61dba1b824ec36bb220ddc:1045837"
    user = get_user_id.get_user_id(slid_token)
    slnet_token = get_slnet_token(slid_token)
    user_info = get_user_info.get_user_info(user,slnet_token)
    print(user_info)
    print(slnet_token)
    print(user)



# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
