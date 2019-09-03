#!/usr/bin/env bash

coverage run --source cad -m unittest
coverage report -i
coverage html -d coverage/html
coverage erase
