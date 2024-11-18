import ee
import geemap
import xarray as xr

ee.Authenticate()
ee.Initialize()

region = ee.Geometry.BBox(150, -20, -75, 20)
oisst = (
    (ee.ImageCollection("NOAA/CDR/OISST/V2_1"))
    .select("sst")
    .filterDate("1995-01-01", "2024-01-01")
    .filterBounds(region)
)

print("downloading...")
ds = geemap.ee_to_xarray(
    oisst, projection=oisst.first().select(0).projection(), geometry=region
) * 0.01 # Raw data downloaded is 100 times the actual value. I don't know why.

ds.to_netcdf("data/oisst.nc", engine="h5netcdf")
print("file saved")
