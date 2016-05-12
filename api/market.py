#!/usr/bin/env python
import datetime
import re
import uuid
import json
import constants
import models
from api.base import BaseApi, authorize
from api.error import Error
from frameworks.bottle import request, response
from utils import request_utils, validation_utils


class MarketApi(BaseApi):
    
    def postBook(self, unum):
        subject = request.forms.get("subject")
        isbn = request.forms.get("isbn")
        title = request.forms.get("title")
        author = request.forms.get("author")
        icon = request.forms.get("icon")
        price = request.forms.get("price")
        owner = unum
        book = models.Book()
        book.subject = subject
        book.isbn = isbn
        book.title = title
        book.author = author
        book.icon = icon
        book.price = price
        book.owner = owner
        book.put()
        return dict(code=200, message="Successfully posted book listing for " + title + ".", valid=True)
    
    def updateBook(self, field, update, unum):
       pass
    
    def updateItem(self, field, update, unum):
        pass

    def postItem(self, unum):
        item = models.Item()
        item.type = request.forms.get("type")
        item.name = request.forms.get("name")
        item.image = request.forms.get("image")
        item.price = request.forms.get("price")
        item.owner = unum
        item.put()
        return dict(code=200, message="Successfully posted item listing for " + request.forms.get("name") + ".", valid=True)
    
    def getBookByISBN(self, isbn):
        return json.dumps(models.Book.get_by_isbn(isbn))
    
    def getBookByAuthor(self, author):
        return json.dumps(models.Book.get_by_author(author))
    
    def getBookBySubject(self, subject):
        book = models.Book.get_by_subject(subject)
        return json.dumps(book)
    
    def getBookByTitle(self, title):
        return models.Book.get_by_title(title)
    
    def getAllBooks(self):
        pass
    
    def getItemsByType(self, type):
        items = list()
        for item in models.Item.get_by_type(type):
            items.append(item)
        items = json.dumps(items)
        return dict(code=200, message=items, valid=True)
    
    def getItemsByName(self, name):
        return models.Item.get_by_name(name)

