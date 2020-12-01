#!/bin/bash

ssh root@68.183.101.22 'rm -r ~/bookstore/fastapi-demo'
scp -r ../fastapi-demo root@68.183.101.22:~/bookstore

ssh root@68.183.101.22 'docker stop bookstore-api'
ssh root@68.183.101.22 'docker rm bookstore-api'

ssh root@68.183.101.22 'docker build -t bookstore-build ~/bookstore/fastapi-demo'
ssh root@68.183.101.22 'docker run -idt -e PORT="3000" -p 3000:3000 --name=bookstore-api bookstore-build'

