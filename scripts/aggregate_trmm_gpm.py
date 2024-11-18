"""
Aggregate TRMM and GPM data for Colombia into a single 
``DataArray`` of ``precipitation`` respectively.
Transpose ``lon`` and ``lat`` dimensions (to ``lat`` first)
save the ``DataArray`` to a new NetCDF file.
"""

import xarray as xr
import rc_rainfall


NETCDF_ENGINE = "h5netcdf"
PARALLEL_OPEN = False
REGION = "Colombia"
unit = "mm/day"

trmm = (
    xr.open_mfdataset(
        "data/TRMM/*.nc4",
        engine=NETCDF_ENGINE,
        parallel=PARALLEL_OPEN,
        preprocess=rc_rainfall.preprocess_trmm_colombia,
    )
    .load()["precipitation"]
    .transpose(..., "lat", "lon")
)

trmm.attrs["units"] = unit

trmm.to_netcdf(f"data/TRMM_{REGION}.nc", engine=NETCDF_ENGINE)

gpm = (
    xr.open_mfdataset(
        "data/GPM/*.nc4",
        engine=NETCDF_ENGINE,
        parallel=PARALLEL_OPEN,
        preprocess=rc_rainfall.preprocess_gpm_colombia,
    )
    .load()["precipitation"]
    .transpose(..., "lat", "lon")
)
gpm.attrs["units"] = unit

gpm.to_netcdf(f"data/GPM_{REGION}.nc", engine=NETCDF_ENGINE)

print("Done")
