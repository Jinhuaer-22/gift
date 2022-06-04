# coding:utf-8

"""
    1: role的修改
    2: active的修改
    3: delete_user

    username 姓名
    role normal or admin
    active True or False
    create_time timestamp
    update_time timestamp
    gifts []

    username:{username, role, gifts}
"""
import json
import os
import time
from common import utils
from common.error import UserExistsError, RoleExistsError, LevelError
from common.utils import timestamp_to_string
from common.consts import ROLES, FIRSTLEVELS, SECONDLEVELS

"""
    1: gifts 奖品结构的确定
    2: gifts 奖品的提取
    3: gifts 奖品的添加
    4: gifts 初始化
      
    { 
        level1：{
            level1：{
                gift_name1：{
                    name: xx
                    count: xx
                },
                gift_name2：{
                    name: xx
                    count: xx
                }
            },
            level2: {}
            level3: {}
        },
        level2：{
            level1：{}
            level2: {}
            level3: {}
            },
        level3：{
            level1：{}
            level2: {}
            level3: {}
        },
        level4：{
            level1：{}
            level2: {}
            level3: {}
        }
    }
     
"""

class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json
        self.__check_user_json()
        self.__check_gift_json()
        self.__init_gifts()

    def __check_user_json(self):
        utils.check_file(self.user_json)

    def __check_gift_json(self):
        utils.check_file(self.gift_json)

    def __read_users(self, time_to_str=False):
        with open(self.user_json, 'r') as f:
            data = json.loads(f.read())

        if time_to_str:
            for username, v in data.items():
                v['create_time'] = timestamp_to_string(v['create_time'])
                v['update_time'] = timestamp_to_string(v['update_time'])
                data[username] = v
        return data

    def __write_user(self, **user):
        if 'username' not in user:
            raise ValueError('missing username')
        if 'role' not in user:
            raise ValueError('missing role')

        user['active'] = True
        user['create_time'] = time.time()
        user['update_time'] = time.time()
        user['gifts'] = []

        users = self.__read_users()
        # print(users)
        # return

        if user['username'] in users:
            raise UserExistsError('username %s had exists' % user['username'])

        users.update(
            {user['username']: user}
        )

        json_users = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_users)

    def __change_role(self, username, role):
        users = self.__read_users()
        user = users.get(username)  # {'username': {role,create_time}}
        if not user:
            return False

        if role not in ROLES:
            raise RoleExistsError('not use role %s' % role)

        user['role'] = role
        user['update_time'] = time.time()
        users[username] = user

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return True

    def __change_active(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        user['active'] = not user['active']
        user['update_time'] = time.time()
        users[username] = user

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return True

    def __delete_user(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False
        delete_user = users.pop(username)

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return delete_user

    def __read_gifts(self):
        with open(self.gift_json) as f:
            data = json.loads(f.read())
        return data

    def __init_gifts(self):
        data = {
            'level1': {
                'level1':{},
                'level2':{},
                'level3':{}
            },
            'level2': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level3': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level4': {
                'level1': {},
                'level2': {},
                'level3': {}
            }
        }

        gifts = self.__read_gifts()
        if len(gifts) != 0:
            return

        json_data = json.dumps(data)
        with open(self.gift_json, 'w') as f:
            f.write(json_data)

    def write_gifts(self, first_level, second_level,
                    gift_name, gift_count):
        if first_level not in FIRSTLEVELS:
            raise LevelError('first level not exists')
        if second_level not in SECONDLEVELS:
            raise LevelError('second level not exists')

        gifts = self.__read_gifts()

        current_gift_pool = gifts[first_level]
        current_second_gift_pool = current_gift_pool[second_level]

        if gift_count <= 0:
            gift_count = 1

        if gift_name in current_second_gift_pool:
            current_second_gift_pool[gift_name] = current_second_gift_pool[gift_name]['count'] + gift_count
        else:
            current_second_gift_pool[gift_name] = {'name': gift_name,
                                                   'count': gift_count
                                                   }

        gifts[first_level] = current_second_gift_pool
        json_data = json.dumps(gifts)
        with open(self.gift_json, 'w') as f:
            f.write(json_data)


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    print(gift_path)
    print(user_path)
    base = Base(user_json=user_path, gift_json=gift_path)

    base.init_gifts()
    #result = base.delete_user(username = 'huahua')
    #print(result)
