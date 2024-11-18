# This script is not fully tested and only here for reference. It is recommended to use ``download_oisst.py`` to download OISST data from Google Earth Engine instead.
#!/bin/zsh

base_url="https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr"
oisst_folder="data/OISST"
mkdir -p "${oisst_folder}"
cd "${oisst_folder}"

for year in $(seq 1994 2023); do
    for month in $(seq -w 01 12); do
        file_list=$(curl -s "${base_url}/${year}${month}/" | grep 'oisst-avhrr-v02r01' | awk -F\" '{print $2}')
        IFS=$'\n'
        for file in ${=file_list}; do
            link="${base_url}/${year}${month}/${file}"
            curl -LJO --url "${link}"
        done
    done
done
