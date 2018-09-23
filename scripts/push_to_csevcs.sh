#!/bin/bash
set -e
git checkout master
git pull git@github.com:dbgrigsby/Postr.git
git push https://csevcs.case.edu/git/eecs395_fall2018_postr.git

