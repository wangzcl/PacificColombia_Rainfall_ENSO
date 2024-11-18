import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import cartopy.io.img_tiles as cimgt
from cartopy.mpl import geoaxes
from . import data_utils


def set_extent_colombia(self: geoaxes.GeoAxes):
    self.set_extent(
        [*data_utils.COLOMBIA_LON_EXTENT, *data_utils.COLOMBIA_LAT_EXTENT],
        crs=cartopy.crs.PlateCarree(),
    )
    return


geoaxes.GeoAxes.set_extent_colombia = set_extent_colombia


def add_country_border(self: geoaxes.GeoAxes, country_name: str, **kwargs):
    countries_shp = shpreader.natural_earth(
        resolution="10m", category="cultural", name="admin_0_countries"
    )
    countries = shpreader.Reader(countries_shp)
    for country in countries.records():
        if country.attributes["NAME"] == country_name:
            return self.add_geometries(country.geometry, ccrs.PlateCarree(), **kwargs)
    raise ValueError(f"Country {country_name} not found in shapefile")


geoaxes.GeoAxes.add_country_border = add_country_border


def set_colombia(self: geoaxes.GeoAxes, linewidth=3):
    self.set_extent_colombia()
    self.coastlines(resolution="10m", linewidth=linewidth)
    self.add_country_border(
        "Colombia",
        facecolor="none",
        edgecolor="black",
        linestyle="--",
        linewidth=linewidth,
    )
    return


geoaxes.GeoAxes.set_colombia = set_colombia
