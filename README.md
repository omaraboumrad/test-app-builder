test-app-builder
================

## Usage

usage: gen.py [-h] [-a APPS] [-m MODELS] [-f MAX_FIELDS] target

    positional arguments:
      target                target django directory

    optional arguments:
      -h, --help            show this help message and exit
      -a APPS, --apps APPS
      -m MODELS, --models MODELS
      -f MAX_FIELDS, --max-fields MAX_FIELDS

## Example

    $ mkdir mysite
    $ python main.py mysite -a 10 -m 100

## Run Tests

    $ python -m unittest tests
