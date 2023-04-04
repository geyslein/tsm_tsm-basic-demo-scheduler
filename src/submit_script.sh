#!/usr/bin/bash

#SBATCH --output=/work/sontsm/%x-%j.out
#SBATCH --error=/work/sontsm/%x-%j.err

python3.9 /home/sontsm/tsm-extractor/src/main.py "$@"




