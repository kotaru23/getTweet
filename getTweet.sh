#!/bin/bash
xargs -I{} sh -c 'echo {} | python getTweets.py ; (cd ./json; zip -q {}.zip {}.json ; rm {}.json)'
