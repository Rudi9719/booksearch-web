# BookSearch API Web
BookSearch is a small startup mainly for SUNY schools where students can exchange their books, and in some cases items without being ripped off by the bookstore.

### IMPORTANT
Due to Google App Engine requirements, [this sdk](https://cloud.google.com/appengine/downloads) is needed to run the application.
+ Ensure that you use JSON data instead of x-www-form-urlencoded. You will get a 500 error.

## Parts
+ Google App Engine
+ main.py  
 - The main class
 - Has all API routes and market/Web routes
+ constants.py
 - Has all constants ~~like sqlite3 connection and cursor~~
+ api
 - Stores API functions
 - Market
   + Where the actual listings live/are created from
   + Actual Books/Items classes are in store

#### Developers
[Rudi9719](http://github.com/Rudi9719) - Rudi  
[Pendent20](http://github.com/Pendent20) - Dakota  
[ezeraneal](http://github.com/ezraneal) - Ezra