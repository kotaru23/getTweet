#!/bin/bash
docker run --rm -v `pwd`/twitter-api-keys/api-keys.toml:/app/key.toml -v ${HOME}/project/sample_screen_name.txt:/app/screen_name.txt -v `pwd`:/app/output/ gettweet
