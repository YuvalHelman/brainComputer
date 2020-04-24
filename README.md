[![Build Status](https://travis-ci.org/YuvalHelman/brainComputer.svg?branch=master)](https://travis-ci.org/YuvalHelman/brainComputer)
[![codecov](https://codecov.io/gh/YuvalHelman/brainComputer/branch/master/graph/badge.svg)](https://codecov.io/gh/YuvalHelman/brainComputer)

# brainComputer 

A containerized based project with a backend that incorporates a message queue, designated server, parsers for 
heavy computation, a DB to store the info and a client that sends data with an implemented API+GUI to view everything


![alt text](https://github.com/YuvalHelman/brainComputer/blob/master/images/project_layout.PNG?raw=true)

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone https://github.com/YuvalHelman/brainComputer.git
    ...
    $ cd brainComputer/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brainComputer] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ ./scripts/test_all.sh
    ...
    ```
   
## Deployment

To deploy all of the containers for a fast start of work using Docker:

   ```sh
    $ ./run-pipeline.sh
   ```
    

You should then use the client module to upload snapshots data into the system 
(using the hardware's format - an example can be downloaded from 
[here](https://storage.googleapis.com/advanced-system-design/sample.mind.gz))

   ```sh
    [brainComputer] $ python -m brainComputer.client upload-sample 
                      path_to_data_file
                      -h 0.0.0.0 -p 8000 
   ```
And lookup on the results from the GUI:
   ```sh
    [brainComputer] $ firefox 0.0.0.0:8080/users/
                      ...
   ```
Or get info from the API:
   ```sh
    [brainComputer] $ python
        >> import requests
        >> requests.get('0.0.0.0:5000/users')
        ...
   ```
## Usage

### Client

The `client` package provides the following interface:

   ```pycon
    >>> from brainComputer.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to server - host:port 
   ```

And the following CLI:

```sh
$ python -m brainComputer.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
```

### Server

The server itself is quite simple: it accepts connections from the client, receives the uploaded samples
 and publishes them to the message queue;
 

The `server` package provides the following interface:

   ```pycon
    >>> from brainComputer.server import run_server
    >>> def print_message(message):
    ...     print(message)
    >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
    … # listen on host:port and pass received messages to publish
   ```

And the following CLI:

```sh
$ python -m brainComputer.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
```

### Parser

The `parser` package provides the following interface:

   ```pycon
    >>> from brainComputer.parsers import run_parser
    >>> data = … 
    >>> result = run_parser('pose', data)
   ```
Which accepts a parser name and some raw data, as consumed from the message queue, and returns the result

And the following CLI:

```sh
$ python -m brainComputer.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
```
which runs the parser exactly once, and:

```sh
$ python -m brainComputer.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'

```
which runs the parser as a service, and works with the message queue indefinitely.

### Saver

The Saver itself is quite simple: it connects to a database, accepts a topic name and some data as consumed from the 
message queue and saves it to the database.
 
The `saver` package provides the following interface:

   ```pycon
    >>> from brainComputer.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)
   ```
Which connects to a database, accepts a topic name and some data, as consumed from the message queue, and saves it to the database.

And the following CLI:

```sh
$ python -m brainComputer.saver save                     \
      -d/--database 'mongodb://127.0.0.1:27017' \
     'pose'                                       \
     'pose.result' 
```
Which accepts a topic name and a path to some raw data, as consumed from the message queue, and saves it to a database.

```sh
$ python -m brainComputer.saver run-saver  \
      'mongodb://127.0.0.1:27017' \
      'rabbitmq://127.0.0.1:5672/'
```
which runs the saver as a service, and works with the message queue indefinitely.

##### The Saver automatically subscribes to all topics published by any valid parser.

### API

The API server supports the following RESTful API endpoints:
- ##### GET /users
- ##### GET /users/{user-id}
- ##### GET /users/{user-id}/snapshots
- ##### GET /users/{user-id}/snapshots/{snapshot-id}
- ##### GET/users/{user-id}/snapshots/{snapshot-id}/{result-name}

The `api` package provides the following interface:

   ```pycon
    >>> from brainComputer.api import run_api_server
    >>> run_api_server(
    ...     host = '127.0.0.1',
    ...     port = 5000,
    ...     database_url = 'mongodb://127.0.0.1:27017',
    ... )
    … # listen on host:port and serve data from database_url
   ```

And the following CLI:

   ```sh
    $ python -m brainComputer.api run-server \
          -h/--host '127.0.0.1'       \
          -p/--port 5000              \
          -d/--database 'mongodb://127.0.0.1:27017'
   ```

### CLI

The CLI consumes the API and simply reflects it:

The `api` package provides the following interface:

   ```pycon
    $ python -m cortex.cli get-users
    …
    $ python -m cortex.cli get-user 1
    …
    $ python -m cortex.cli get-snapshots 1
    …
    $ python -m cortex.cli get-snapshot 1 2
    …
    $ python -m cortex.cli get-result 1 2 'pose'
    …
   ```

All commands accepts the -h/--host and -p/--port flags to configure the host and port,
but default to the API's address.

The `get-result` command also accept the -s/--save flag that, if specified,
receives a path, and saves the result's data to that path.

### GUI

The GUI is a standalone server that reflects the API in a more pleasant way, implemented with Flask, 
bootstrap and basic HTML\CSS.

The `gui` package provides the following interface:

   ```pycon
    >>> from cortex.gui import run_server
    >>> run_server(
    ...     host = '127.0.0.1',
    ...     port = 8080,
    ...     database_url = 'mongodb://127.0.0.1:27017',
    ... )
   ```

And the following CLI:

   ```sh
    $ python -m cortex.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -d/--database 'mongodb://127.0.0.1:27017'
   ```


## Adding new Parsers

We use an "Aspect oriented programming" for ease of use.
After implementing a new parser Class\Function it's automatically possible to run it as a service and invoke it 
like the other parsers. 

Adding new parsers should be done in the following manner:
- Add a new file to hold your parser's code under 'brainComputer/parsers/', or use one of the files already in there.
- The new parser's name should start with 'parse_' if it's a function, or end with 'Parser' if it's a Class. 
  In the case of a class, it has to have a "parse" function in it to do the parsing. the functions should have a certain
signature.
- There has to be a 'field' member to your function\Class that indicates the type of parsing data it returns.

- Example:
    ```pycon
   def parse_function(snapshot):
        pass
   parse_function.field = 'translation'

   class ClassParser:
       field = 'color_image'

       def parse(self,snapshot)
           pass
    ```

- The framework will automatically collect your function and use it for the functionality that's provided in it's 'field' member. 
- A functionality (e.g 'field' member) may have only one function for it and thus if more than one is implemented, one of them will be chosen arbitrarily.
- A parser should return an encoded json object of the following json format, or assist the given function:
 ```pycon
{ 'user': {'user_id': '...' , '...' }
   'snapshots'= [
                 {'datetime': '..', parsedResult }
                ]
}
 ``` 
Or use this builtin function to avoid mistakes:
 ```pycon
 from brainComputer.parsers.utils import formatted_encoded_one_data
 ```



