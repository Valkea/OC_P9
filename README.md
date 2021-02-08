# LITReview

This project aims to build a community around the idea of reading and asking books and articles' reviews.

The version currently available in this Git Repo is a Minimal Viable Product built to run locally.

## Installation

In order to use this project locally, you need to follow the steps below:

### First, 
let's duplicate the project github repository

```bash
>>> git clone https://github.com/Valkea/OC_P9.git
>>> cd OC_P9
```

### Secondly,
let's create a virtual environment and install the required Python libraries

(Linux or Mac)
```bash
>>> python3 -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

(Windows):
```bash
>>> py -m venv venv
>>> .\venv\Scripts\activate
>>> py -m pip install -r requirements.txt
```

## Running the project

Once installed, the only command required to use the project is the following one

```bash
>>> python manage.py runserver
```

## Using the project

### as an admin

visit *http://127.0.0.1:8000/zadmin* and use the demo credentials to access the admin content:

*demo-login :* supadmin

*demo-password :* demopass

**this account need to be removed / changed before going into production !**

Once in the admin, you will be able to add, edit or remove 'users', 'tickets' and 'reviews'.

In the 'Ticket' section you can preview & access the linked 'Review' (if any).
In the 'User' section you can indeed manage the user's informations but you can also see and edit followed and following users as-well.


### as a reviewer

visit *http://127.0.0.1:8000* and use the one of the demo credentialss below:

#### Alice
```
Alice is an account with two opened tickets and one review.
She is not following any user, and she is not followed by anyone.

So she is supposed to see its own tickets & reviews only
(unless you make some modifications on any of the accounts).
```

*demo-login :* Alice

*demo-password :* merveille


#### Bob
```
Bob is an account with some opened tickets & reviews.
He is not following anyone but he is followed by Carl.

So he is supposed to see its own tickets & reviews as well as
the reviews wrote by Carl on tickets he (Bob) opened
(unless you make some modifications on any of the accounts).
```

*demo-login :* Bob	

*demo-password :* monstres


#### Carl
```
Carl is an account with some opened tickets & reviews.
He is following Bob and he is not followed by anyone.

So he is supposed to see its own tickets & reviews as
well as the reviews & tickets wrote by Bob
(unless you make some modifications on any of the accounts).
```

*demo-login :* Carl	

*demo-password :* hal9000!

## Statics & Medias

The uploaded pictures are stored in the "media" folder. They are automatically removed when replaced in a ticket or whenever the review is removed.

The CSS & HTML files are stored in the 'static' & 'template' folders in the root (when global) or in their respective application folders (when tied to a specific application).


## Documentation

The applications views are documented using the Django admindoc format.
However the admindoc module is not activated at the moment.


## PEP8

The project was developped using 'vim-Flake8' and 'black' modules to enforce the PEP8 rules.


## License
[MIT](https://choosealicense.com/licenses/mit/)
