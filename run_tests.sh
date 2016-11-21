#!/bin/bash

# Replace domain and key with your own. Note that it requires admin access.
# Do not worry about data corruption. These tests will create a custom volume
# for test purposes.
py.test \
    --sxcl-domain=192.168.122.71 \
    --sxkey-path=~/.sx/local/auth/default \
    "$@"
