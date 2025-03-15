#!/bin/bash

curl -OL https://edu.postgrespro.com/demo-small-en.zip

mkdir -p init/sql
unzip demo-small-en.zip -d init/sql/
