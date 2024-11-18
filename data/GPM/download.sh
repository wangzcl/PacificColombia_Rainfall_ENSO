#!/bin/zsh

# run this script in the directory where you want to download the data

# Read each line in the URL file, removing any carriage return characters
while IFS= read -r url; do
    trimmed_url="${url//$'\r'/}" # Remove carriage returns if file originated from Windows
    curl -n -g -c "~/.urs_cookies" -b "~/.urs_cookies" -LJO --url "$trimmed_url"
done < "link.txt"