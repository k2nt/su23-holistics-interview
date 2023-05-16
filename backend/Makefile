# Load environent variables
include .local.env
export $(shell sed 's/=.*//' .env)


SHELL := /bin/zsh


# HELP =================================================================================================================
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
.DEFAULT_GOAL := help


run:  # Run backend service locally
	flask run
.PHONY: run
