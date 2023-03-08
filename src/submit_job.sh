#!/usr/bin/env bash

name="$1"
sbatch --job-name="$name" _submit_script.sh "$*"

