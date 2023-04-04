#!/bin/bash

# This is a helper script to allow
# any command or script be passed
# to an earlier `exec $@`

set -x
exec "$@"