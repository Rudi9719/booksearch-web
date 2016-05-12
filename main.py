#!/usr/bin/env python
import logging

from api.user import UserApi
from api.error import Error
from api.market import MarketApi
from frameworks.bottle import Bottle, response, run, static_file, route, request, template, Router, HTTPError

from controller.home import HomeController
from controller.static import StaticController

from os.path import join, dirname

# Setup App
app = Bottle()


#Setup APIs below
market = MarketApi()
user_api = UserApi()

#Setup Controllers
home_controller = HomeController()
static_controller = StaticController()


#Handle errors
@app.error(code=400)
@app.error(code=401)
@app.error(code=405)
@app.error(code=406)
@app.error(code=409)
@app.error(code=501)
@app.error(code=502)
def handle_error(error):
    return Error.handle_error(response, error)

@app.error(code=404)
def handle_404(error):
    logging.error(error.traceback)
    return template('error/404')

@app.error(code=500)
def handle_500(error):
    logging.error(error.traceback)
    return template('error/500')

@app.error(code=403)
def handle_403(error):
    logging.error(error.traceback)
    return template('error/403')


class SubdomainRouter(Router):
    def match(self, environ):
        domain = environ.get('HTTP_HOST') or environ.get('SERVER_NAME')
        path = environ['PATH_INFO']
        if domain:
            if ':' in domain:
                domain = domain.split(':')[0]
            environ['PATH_INFO'] = '/%s%s' % (domain, path)
        try:
            match = Router.match(self, environ)
            return match
        except HTTPError as e:
            if e.status_code == 404:
                environ['PATH_INFO'] = path
                return Router.match(self, environ)
        finally:
            environ['PATH_INFO'] = path

app.router = SubdomainRouter()



def main():
    # System Routes
    
    
    # Static Routes - /static/styles.css
    app.route("/static/<filename>", method="GET", callback=static_controller.file)
    app.route("/static/<folder>/<filename>", method="GET", callback=static_controller.fileOnePath)
    app.route("/static/<folder1>/<folder2>/<filename>", method="GET", callback=static_controller.fileTwoPath)
    app.route("/static/<folder1>/<folder2>/<folder3>/<filename>", method="GET", callback=static_controller.fileThreePath)
    
    # API Routes
    
    # Users
    app.route("/api/users/register/<unum>", method="POST", callback=user_api.create)
    app.route("/api/users/login", method="POST", callback=user_api.login)
    app.route("/api/users/logout", method="POST", callback=user_api.logout)
    app.route("/api/users/forgot-password", method="POST", callback=user_api.forgot_password)
    app.route("/api/users/reset-password", method="POST", callback=user_api.reset_password)
    app.route("/api/users/change-password", method="POST", callback=user_api.change_password)
    #app.route("/api/users/get/<unum>"), method="GET", callback=user_api.get_user) #TODO: Implement method lol


    # Market Routes
    app.route("/market", method="GET", callback=None)
    app.route("/market/search/books/by/author/<author>", method="GET", callback=market.getBookByAuthor)
    app.route("/market/search/books/by/isbn/<isbn>", method="GET", callback=market.getBookByISBN)
    app.route("/market/search/books/by/subject/<subject>", method="GET", callback=market.getBookBySubject)
    app.route("/market/search/books/by/title/<title>", method="GET", callback=market.getBookByTitle)
    app.route("/market/search/items/by/type/<type>", method="GET", callback=market.getItemsByType)
    app.route("/market/search/items/by/name/<name>", method="GET", callback=market.getItemsByName)

    
    
    app.route("/market/post/book/<unum>", method="POST", callback=market.postBook)
    app.route("/market/post/item/<unum>", method="POST", callback=market.postItem)
    
    
    ##TODO Create market_controller.py and actually build website
    # Web routes
    app.route("/", method="GET", callback=home_controller.index)
    app.route("/login", method="GET", callback=home_controller.login)
    app.route("/suny", method="GET", callback=home_controller.suny)
    app.route("/about", method="GET", callback=home_controller.about)
    app.route("/discover", method="GET", callback=home_controller.discover)
    app.route("/help", method="GET", callback=home_controller.help)
    app.route("/contact", method="GET", callback=home_controller.contact)
    #app.route("/web/market", method="GET", callback=market_controller.index)
   
   
   # In order to change port to 80, you must first run as sudo
   # host = bind address. 0.0.0.0 for all adresses on port, or URL
   # Debug gives some info
   # app.run(host='0.0.0.0', port=8080, debug=True)



if __name__ == "main" or __name__ == "__main__":
    main()


