#!/usr/bin/env zsh

# This script takes two arguements, the name of the lambda function and the name of the input directory

# Check if zip file exists
if [ -f "$2.zip" ]; then
    rm "$2.zip"
fi

cd "$2"

# zip the contents of the input directory without the directory itself
zip -r -D $2.zip *

# upload the zip file to the lambda function
aws lambda update-function-code --function-name $1 --zip-file fileb://$2.zip


