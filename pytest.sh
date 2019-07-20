#!/usr/bin/env bash

coverage run --source cad -m unittest
coverage report -m -i
coverage html -d coverage/html
coverage erase
