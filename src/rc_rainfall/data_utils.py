from importlib import resources
import numpy as np
import xarray as xr
import pandas as pd
import geopandas as gpd
import regionmask

COLOMBIA_LAT_EXTENT = (-5, 13)
COLOMBIA_LON_EXTENT = (-80, -66)
COLOMBIA_BOX = {"lat": slice(*COLOMBIA_LAT_EXTENT), "lon": slice(*COLOMBIA_LON_EXTENT)}
COLOMBIA_CENTER = {"lat": 4.5, "lon": -74}

NINO34_LAT_EXTENT = (-5, 5)
NINO34_LON_EXTENT = (190, 240)
NINO34_BOX = {"lat": slice(*NINO34_LAT_EXTENT), "lon": slice(*NINO34_LON_EXTENT)}

def add_trmm_time(x: xr.DataArray | xr.Dataset, time_attr_name="BeginDate"):
    """Add time coordinate to TRMM data."""
    time_str = x.attrs[time_attr_name]
    time_index = pd.to_datetime([time_str])
    return x.expand_dims(
        dim={"time": time_index},
        axis=0,
    )


def preprocess_trmm(
    x: xr.DataArray | xr.Dataset, lat: float | slice, lon: float | slice
):
    """Preprocess TRMM data. Used in ``xarray.open_mfdataset``."""
    x = x.sel(lat=lat, lon=lon)
    x = add_trmm_time(x)
    return x


def preprocess_trmm_colombia(x: xr.DataArray | xr.Dataset):
    """Preprocess TRMM data for Colombia. Used in ``xarray.open_mfdataset``."""
    return preprocess_trmm(x, **COLOMBIA_BOX)


def preprocess_gpm_colombia(x: xr.DataArray | xr.Dataset):
    """Preprocess GPM data for Colombia. Used in ``xarray.open_mfdataset``."""
    return x.sel(**COLOMBIA_BOX)


def xr_region_mask(x: xr.DataArray | xr.Dataset, country: str) -> xr.DataArray:
    """Create a boolean mask of a country for a given xarray object."""
    countries = regionmask.defined_regions.natural_earth_v5_1_2.countries_50
    mask = countries.mask(x) == countries.map_keys(
        country
    )
    return mask

def colombia_pacific_shapefile():
    return (
        resources.files("rc_rainfall")
        / "data/Colombia_Pacific_shapefile/colombia_pacific.shp"
    )

def xr_mask_pacific(x: xr.DataArray | xr.Dataset) -> xr.DataArray:
    """Create a boolean mask of the Pacific region for a given xarray object."""
    colombia_pacific_region = gpd.read_file(
       colombia_pacific_shapefile()
    )
    pacific_region_mask = regionmask.mask_geopandas(
        colombia_pacific_region, x
    ) == 0
    return pacific_region_mask

def latitudinal_weight(x: xr.DataArray | xr.Dataset) -> xr.DataArray:
    """Weights of the data by latitude."""
    weights = np.cos(np.deg2rad(x.coords["lat"]))
    weights.name = "weights"
    return weights


def spatial_mean_series(x: xr.DataArray, weights: xr.DataArray) -> pd.Series:
    return x.weighted(weights).mean(("lat", "lon")).to_series()

def anomaly(x: xr.DataArray | xr.Dataset) -> xr.DataArray | xr.Dataset:
    """Calculate the anomaly of the data."""
    return x.groupby(
       x.index.month
    ).transform(lambda x: x - x.mean())
