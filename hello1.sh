#!/bin/bash

input_file="/Users/kuchetti.mahesh/Desktop/myproject/access.log"
success_file="/Users/kuchetti.mahesh/Desktop/myproject/success.txt"
error_file="/Users/kuchetti.mahesh/Desktop/myproject/error.txt"

# Remove the existing output file if it exists
if [ -e "$success_file" ]; then
    rm "$success_file"
fi
if [ -e "$error_file" ]; then
    rm "$error_file"
fi

# Process each line in the input file
while IFS= read -r line; do
    u=$(echo "$line" | awk -F' ' '{print $1}')
    v=$(echo "$line" | awk -F'"' '{print $2}')
    w=$(echo "$line" | grep -oE '\s\d{3}\s' )
    if [ $w -gt 399 ]
    then
        echo "$u,$v,$w" >>"$error_file" 
    else      
        echo "$u,$v,$w" >> "$success_file"
    fi
done < "$input_file"
