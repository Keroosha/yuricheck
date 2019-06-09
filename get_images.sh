#!/bin/bash

set -e -u

mkdir -p image
cd image

for i in $(seq 60000 60255)
do
    curl -sO "https://www.thiswaifudoesnotexist.net/example-$i.jpg" &
done
