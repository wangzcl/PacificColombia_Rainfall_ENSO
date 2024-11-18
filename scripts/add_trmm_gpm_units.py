import xarray as xr

NETCDF_ENGINE = "h5netcdf"
REGION = "Colombia"

trmm = xr.open_dataarray(f"data/TRMM_{REGION}.nc", engine=NETCDF_ENGINE)
gpm = xr.open_dataarray(f"data/GPM_{REGION}.nc", engine=NETCDF_ENGINE)
unit = "mm/day"
trmm.attrs["units"] = unit
gpm.attrs["units"] = unit

trmm.to_netcdf(f"data/TRMM_{REGION}_n.nc", engine=NETCDF_ENGINE)
gpm.to_netcdf(f"data/GPM_{REGION}_n.nc", engine=NETCDF_ENGINE)
