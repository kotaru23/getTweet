#!/bin/bash

docker run get-tweet --rm  -v $1:/app/key.toml -v $2:/app/screen_name.txt -v $3:/app/output/

