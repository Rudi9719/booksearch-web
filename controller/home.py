#!/usr/bin/env python

from controller.base import BaseController
from frameworks.bottle import view, static_file, template
class HomeController(BaseController):
    
    
    
    def index(self):
        return template('home/index')
    
    def login(self):
        return template('home/login')
    
    def about(self):
        return template('home/about')
    
    def help(self):
        return template('home/help')
    
    def discover(self):
        return template('home/discover')
    
    def contact(self):
        return template('home/contact')
    
    @view('home/suny')
    def suny(self):
        pass

