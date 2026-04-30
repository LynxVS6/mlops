#!/bin/sh
set -e

curl http://127.0.0.1:5003/invocations \
  -H "Content-Type:application/json" \
  --data '{"inputs": [[-1.75938045, -1.2340347, -1.41327673, 0.76150439, 2.20097247, -0.10937195, 0.58931542, 0.1135538]]}'
