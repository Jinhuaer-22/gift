# coding:utf-8

"""
    1: admin类的搭建
    2: 获取用户函数（包含获取身份）
    3: 添加用户（判断当前身份是否是管理员）
    4: 冻结与恢复身份
    5: 修改用户身份
"""
"""
    1: admin的验证（只有admin的用户才能用这个类）
    2: 任何函数都应该动态的更新getuser
    3: 奖品的添加
    4: 奖品的删除
    5: 奖品数量的更新（同步base调整）
"""

import os

from common.error import NotUserError,UserActiveError, RoleError

from base import Base


class Admin(Base):
    def __init__(self, user_name, user_json, gift_json):
        self.user_name = user_name
        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.user_name)
        if current_user == None:
            raise NotUserError('Not user %s' % self.user_name)

        if current_user.get('active') == False:
            raise UserActiveError('the user %s had not used' % self.user_name)

        if current_user.get('role') != 'admin':
            raise RoleError('permission by admin')

        self.user = current_user
        self.role = current_user.get('role')
        self.name = current_user.get('username')
        self.active = current_user.get('active')

    def __check(self, message):
        self.get_user()
        if self.role != 'admin':
            raise Exception(message)

    def add_user(self, username, role):
        self.__check('permission')
        self._Base__write_user(username=username, role=role)

    def update_user_active(self, username):
        self.__check('permission')
        self._Base__change_active(username=username)

    def update_user_role(self, username, role):
        self.__check('permission')
        self._Base__change_role(username=username, role=role )

    def add_gift(self, first_level, second_level,
                      gift_name, gift_count):
        self.__check('permission')
        self._Base__write_gifts(first_level, second_level,
                                gift_name, gift_count)

    def delete_gift(self, first_level, second_level, gift_name):
        self.get_user()
        self.__check('permission')
        self._Base__delete_gift(first_level, second_level,gift_name)

    def update_gift(self, first_level, second_level,
                    gift_name, gift_count):
        self.__check('permission')
        self._Base__gifts_update(first_level, second_level,
                                 gift_name, gift_count, True)
if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    admin = Admin(user_name='huahua', user_json=user_path, gift_json=gift_path)
    # admin.get_user()
    # print(admin.name, admin.role)
    # admin.update_user_role('小花', 'normal')
    # admin.delete_gift('level1', 'level2', 'xiaomi')
    admin.update_gift('level2', 'level3', 'ipad', 15)

