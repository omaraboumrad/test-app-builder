test-app-builder
================

## Usage

usage: main.py [-h] [-a APPS] [-m MODELS] target

positional arguments:
  target                target django directory

optional arguments:
  -h, --help            show this help message and exit
  -a APPS, --apps APPS
  -m MODELS, --models MODELS

## Example

> $ mkdir mysite
> $ python main.py mysite -a 10 -m 100

## Run Tests

> $ python -m unittest tests
