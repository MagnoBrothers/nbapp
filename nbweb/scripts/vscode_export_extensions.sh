#!/usr/bin/env bash
echo "Exporting currently installed extensions to '$1'."
if [ -f "$1" ]; then
    echo "File $1 already exists. Please remove file with 'rm $1' and rerun command."
    exit 126
else
    code --list-extensions > $1
fi
