# coding:utf-8

"""
    1: admin类的搭建
    2: 获取用户函数（包含获取身份）
    3: 添加用户（判断当前身份是否是管理员）
    4: 冻结与恢复身份
    5: 修改用户身份
"""
import os

from common.error import NotUserError,UserActiveError

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

        self.user = current_user
        self.role = current_user.get('role')
        self.name = current_user.get('username')
        self.active = current_user.get('active')



if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    admin = Admin(user_name='huahua', user_json=user_path, gift_json=gift_path)
    # admin.get_user()
    print(admin.name, admin.role)

