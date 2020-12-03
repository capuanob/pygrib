import pygrib
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.testing.compare import compare_images

grbs = pygrib.open('../sampledata/eta.grb')
grb = grbs.select(parameterName='Pressure',typeOfLevel='surface')[0]
data = grb.values
lats, lons = grb.latlons()

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.LambertConformal(globe=globe,central_longitude=grb.projparams['lon_0'],
     central_latitude=grb.projparams['lat_0'],
     standard_parallels =(grb.projparams['lat_1'],grb.projparams['lat_2']))
ax = plt.axes(projection=pj)
coords = pj.transform_points(                                                                
         ccrs.PlateCarree(), np.asarray([lons[0,0],lons[-1,-1]]), np.asarray([lats[0,0],lats[-1,-1]]))
ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
ax.scatter(lons.flat,lats.flat,3,marker='o',color='k',zorder=10,transform=ccrs.PlateCarree())
ax.coastlines()
coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,15)
plt.title('Lambert Conformal Model Grid')
# raise exception if generated image doesn't match baseline 
plt.savefig('lambert.png')
assert( compare_images('lambert_baseline.png','lambert.png',10) is None )
plt.show()
