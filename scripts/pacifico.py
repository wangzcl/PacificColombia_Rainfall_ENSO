"""
Generate Pacifico shapefile.
"""

import geopandas as gpd
import os

colombia_municipio = gpd.read_file(
    "data/col-administrative-divisions-shapefiles/col_admbnda_adm2_mgn_20200416.shp"
)

municipio_PCODE = [
    f"CO{n}"
    for n in [
        "52835",
        "52079",
        "52520",
        "52621",
        "52427",
        "52473",
        "52490",
        "52390",
        "52250",
        "52696",
        "19318",
        "19809",
        "19418",
        "76109",
        "27250",
        "27361",
        "27077",
        "27450",
        "27745",
        "27491",
        "27430",
        "27205",
        "27580",
        "27810",
        "27135",
        "27025",
        "27495",
        "27160",
        "27787",
        "27600",
        "27050",
        "27413",
        "27001",
        "27245",
        "27425",
        "27075",
        "27099",
        "05873",
        "05475",
        "27150",
        "27372",
        "27615",
    ]
] # 27073 and 27660 may also worth including

colombia_municipio_pacific = colombia_municipio[
    colombia_municipio["ADM2_PCODE"].isin(municipio_PCODE)
]

colombia_pacific = colombia_municipio_pacific.dissolve().drop(
    columns=[
        "Shape_Leng",
        "Shape_Area",
        "ADM2_ES",
        "ADM1_PCODE",
        "ADM2_REF",
        "ADM2ALT1ES",
        "ADM2ALT2ES",
        "ADM1_ES",
        "ADM2_PCODE",
    ]
)

dir = "data/Colombia_Pacific_shapefile"

if not os.path.exists(dir):
    os.makedirs(dir)
colombia_pacific.to_file(f"{dir}/colombia_pacific.shp")
