# coding:utf-8


class NotPathError(Exception):
    def __init__(self, message):
        self.message = message


class FormatError(Exception):
    def __init__(self, message):
        self.message = message


class NotFileError(Exception):
    def __init__(self, message):
        self.message = message


class UserExistsError(Exception):
    def __init__(self, message):
        self.message = message

class RoleExistsError(Exception):
    def __init__(self, message):
        self.message = message

class LevelError(Exception):
    def __init__(self, message):
        self.message = message