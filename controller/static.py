#!/usr/bin/env python
from controller.base import BaseController
from api.error import Error
from frameworks.bottle import Bottle, response, static_file

class StaticController(BaseController):

    def file(self, filename):
        return static_file(filename, root='static/')

    def fileOnePath(self, folder, filename):
        return static_file(filename, root='static/' + folder + '/')
            
    def fileTwoPath(self, folder1, folder2, filename):
        return static_file(filename, root='static/' + folder1 + '/' + folder2 + '/')
    
    def fileThreePath(self, folder1, folder2, folder3, filename):
        return static_file(filename, root='static/' + folder1 + '/' + folder2 + '/' + folder3 + '/')