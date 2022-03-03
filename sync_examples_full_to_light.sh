#!/bin/bash

# Script to create the perturbo-examples-light based on the perturbo-examples-full folder
#
# Launch in one directory above perturbo-examples-full

SOURCE="./perturbo-examples-full/"
TARGET=$HOME"/github/perturbo-examples-light"

rsync -a --stats --progress --delete \
--filter "- References" \
--filter "- *.h5" \
--filter "- .git" \
$SOURCE $TARGET
