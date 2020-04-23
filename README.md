[![Build Status](https://travis-ci.org/YuvalHelman/brainComputer.svg?branch=master)](https://travis-ci.org/YuvalHelman/brainComputer)
[![codecov](https://codecov.io/gh/YuvalHelman/brainComputer/branch/master/graph/badge.svg)](https://codecov.io/gh/YuvalHelman/brainComputer)
[![Documentation Status](https://readthedocs.org/projects/braincomputeryh/badge/?version=latest)](https://braincomputeryh.readthedocs.io/en/latest/?badge=latest)

# brainComputer 

A containerized based project with a backend that incorporates a message queue, designated server, parsers for 
heavy computation, a DB to store the info and a client that sends data with an implemented API+GUI to view everything

See [full documentation](https://advanced-system-design-foobar.readthedocs.io/en/latest/).

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
    [brainComputer] $ python -m brainComputer.gui run-server
                      ...
   ```
Or get info from the API:
   ```sh
    [brainComputer] $ python
        >> import requests
        >> requests.get('0.0.0.0:8080/users')
        ...
   ```
## Usage

### Client

The `Client` package provides the following interface:

   ```pycon
    >>> from brainComputer.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to server - host:port 
   ```

And the following CLI:

```sh
$ python -m cortex.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
```

### Server

The `Server` package provides the following interface:
   
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `foo` command, with the `run`, `add` and `inc`
subcommands:

```sh
$ python -m webUtils upload -a 127.0.0.1:5000 -u 1 -t message
message sent
$ python -m run_server -a 127.0.0.1:5000 -d ./data
server is ready to recieve requests
$ python -m web -a 127.0.0.1:5000 -d ./data
webserver is ready to recieve requests

3:
```

The CLI further provides the `bar` command, with the `run` and `error`
subcommands.

Curiously enough, `bar`'s `run` subcommand accepts the `-o` or `--output`
option to write its output to a file rather than the standard output, and the
`-u` or `--uppercase` option to do so in uppercase letters.

```sh
$ python -m foobar bar run
bar
$ python -m foobar bar run -u
BAR
$ python -m foobar bar run -o output.txt
$ cat output.txt
BAR
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `foobar`, not `foo` or
`bar`.

```sh
$ python -m foobar bar run -q # this doesn't work
ERROR: no such option: -q
$ python -m foobar -q bar run # this does work
```

To showcase these options, consider `bar`'s `error` subcommand, which raises an
exception:

```sh
$ python -m foobar bar error
ERROR: something went terribly wrong :[
$ python -m foobar -q bar error # suppress output
$ python -m foobar -t bar error # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```


## Adding new Parsers

We use an "Aspect oriented programming" for ease of use.
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
- Adding new functionalities should be done in the 'utils' module.
- A functionality (e.g 'field' member) may have only one function for it and thus if more than one is implemented, one of them will be chosen arbitrarily.
- A parser should return an encoded json object of the following json format, or assist the given function:
 ```pycon
{ 'user': {'user_id': '...' , '...' }
   'snapshots'= [
                 {'datetime': '..', parsedResult }
                ]
}
 ``` 
Or use this builtin function:
 ```pycon
 from brainComputer.utils import formatted_encoded_one_data
 ```



