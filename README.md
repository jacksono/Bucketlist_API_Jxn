[![Build Status](https://travis-ci.org/jacksono/Bucketlist_API_Jxn.svg?branch=develop)](https://travis-ci.org/jacksono/Bucketlist_API_Jxn)
[![Coverage Status](https://coveralls.io/repos/github/jacksono/Bucketlist_API_Jxn/badge.svg?branch=develop)](https://coveralls.io/github/jacksono/Bucketlist_API_Jxn?branch=develop)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/8e4ded420a0c437da424430ddbca1ac3/badge.svg)](https://www.quantifiedcode.com/app/project/8e4ded420a0c437da424430ddbca1ac3)
![alt text](https://img.shields.io/badge/python-3.4-blue.svg)
[![DUB](https://img.shields.io/dub/l/vibe-d.svg)]()


# Bucketlist_API_Jxn
A BucketList Application API
This API allows you to create, edit, view and delete bucketlists and items in a bucketlist.

According to the [Oxford Dictionary](http://www.oxforddictionaries.com/definition/english/bucket-list),
a *bucket list* is a *number of experiences or achievements that a person hopes
to have or accomplish during their lifetime*.

## How to Install and Set it up
Clone the repo from GitHub:
```
$ git clone https://github.com/jacksono/Bucketlist_API_Jxn.git
```

Navigate to the root folder of the repo:
```
$ cd Bucketlist_API_Jxn
```

Install the required packages:
```
$ pip install -r requirements.txt
```

Initialize, migrate, and upgrade the database:
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

## How to run the API
Run the command 
```
$ python start.py
```
You may use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) for Google Chrome to run the API.

## API Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1/` | GET  | The index | FALSE |
| `/api/v1/auth/register/` | POST  | User registration | FALSE |
|  `/api/v1/auth/login/` | POST | User login | FALSE |
| `/api/v1/bucketlists/` | GET, POST | A user's bucket lists | TRUE |
| `/api/v1/bucketlists/<id>/` | GET, PUT, DELETE | A single bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/` | GET, POST | Items in a bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/<item_id>/` | GET, PUT, DELETE| A single bucket list item | TRUE |

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |

## Screenshots

To register a new user:
<img width="1048" alt="screen shot 2017-07-06 at 10 07 10" src="https://user-images.githubusercontent.com/4943363/27900140-c1340304-6235-11e7-8d6d-7e8ec16ffb3b.png">

To log the user in:
<img width="1048" alt="screen shot 2017-07-06 at 10 08 05" src="https://user-images.githubusercontent.com/4943363/27900188-04baaed4-6236-11e7-80eb-4fb06f7cb512.png">

To add a new bucketlist (use the token in the login page in the header):
<img width="1018" alt="screen shot 2017-07-06 at 10 12 37" src="https://user-images.githubusercontent.com/4943363/27900229-2b864384-6236-11e7-9b16-dd6c388dd364.png">

To add a new bucketlist item (use the token in the login page in the header):
<img width="801" alt="screen shot 2017-07-06 at 10 22 06" src="https://user-images.githubusercontent.com/4943363/27900279-6897b780-6236-11e7-8be5-7a032a6645a7.png">

## How to test
To test, run the following command:
```
$ nosetests
```

## Built With...
* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.4/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

## Credits and License

Copyright (c) 2017 [Jackson Onyango](https://github.com/jacksono)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
