"""
Aggregate TRMM Monthly data for Colombia into a single 
``DataArray`` of ``precipitation`` respectively.
Rename ``nlon`` and ``nlat`` dimensions to ``lon`` and ``lat``.
Transpose ``lon`` and ``lat`` dimensions (to ``lat`` first)
save the ``DataArray`` to a new NetCDF file.
"""
import xarray as xr
import pandas as pd


NETCDF_ENGINE = "h5netcdf"
PARALLEL_OPEN = False
REGION = "Colombia"

def preprocess_trmm_monthly(x: xr.DataArray | xr.Dataset):
    attr_list = x.attrs["FileHeader"].split(";\n")
    attr_dict = {item.split("=")[0]: item.split("=")[1] for item in attr_list if "=" in item}
    time_str = attr_dict["StartGranuleDateTime"]
    time_datetime = pd.to_datetime(time_str).to_datetime64()
    time_index = pd.DatetimeIndex([time_datetime])
    x = x.expand_dims(
        dim={"time": time_index},
        axis=0,
    )
    return x

trmm_monthly = (
    xr.open_mfdataset(
        "data/TRMM_Monthly/*.nc4",
        engine=NETCDF_ENGINE,
        parallel=PARALLEL_OPEN,
        preprocess=preprocess_trmm_monthly,
    )
    .load()["precipitation"]
    .transpose(..., "nlat", "nlon")
)


trmm_monthly = trmm_monthly.rename({"nlon": "lon", "nlat": "lat"})

trmm_monthly.to_netcdf(f"data/TRMM_Monthly_{REGION}.nc", engine=NETCDF_ENGINE)

print("Done")
