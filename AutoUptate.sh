#!/bin/bash
git add .
git commit
git pull
git submodule update --remote
git push