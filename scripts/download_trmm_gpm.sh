#!/bin/zsh

cd "data"
save_dirs=("TRMM" )
for save_dir in "${save_dirs[@]}"; do
    mkdir -p "$save_dir"
    cd "$save_dir"
    # Read each line in the URL file
    while IFS= read -r url; do
        trimmed_url="${url//$'\r'/}" # Remove carriage in each line of the file
        curl -n -g -c "~/.urs_cookies" -b "~/.urs_cookies" -LJO --url "$trimmed_url"
    done < "link.txt" # link.txt is the file containing the URLs, downloaded from disc.gsfc.nasa.gov
done
