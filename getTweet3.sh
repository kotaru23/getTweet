#!/bin/bash
xargs -I{} sh -c 'echo {} | python3 getTweets.py ; (cd ./json; zip -q {}.zip {}.json ; rm {}.json )'
