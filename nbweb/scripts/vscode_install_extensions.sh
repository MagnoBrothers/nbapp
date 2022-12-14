#!/usr/bin/env bash

cat $1 | while read extension || [[ -n $extension ]];
do
  code --install-extension $extension --force &
done
