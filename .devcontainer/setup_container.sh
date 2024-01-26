#!/usr/bin/env bash


hatch config set dirs.env.virtual $PWD/.virtualenvs
hatch env create