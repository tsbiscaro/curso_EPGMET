#plota um PPI georeferenciado
import matplotlib.pyplot as plt
import pyart
import cartopy.crs as ccrs
import numpy as np


radar = pyart.aux_io.read_gamic('JG1-20220816234803.HDF5')


#cantos da imagem
#tamanho da imagem - 5 x 5 graus (raio de 250 km)
sz = 5.0

lat0 = radar.latitude['data'][0] - sz/2
lat1 = radar.latitude['data'][0] + sz/2
lon0 = radar.longitude['data'][0] - sz/2
lon1 = radar.longitude['data'][0] + sz/2
#centro da imagem
lat_radar, lon_radar = radar.latitude['data'][0], radar.longitude['data'][0]


fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

display = pyart.graph.RadarMapDisplay(radar)

#vamos criar 3 grid lines com o centro no radar
dl = sz/4
lon_lines=np.arange(lon0, lon1, dl)
lat_lines=np.arange(lat0, lat1, dl)

#plota o ppi sobre um mapa
#sweep = 0 -> primeiro PPI, sweep = 1 -> segundo PPI, etc

display.plot_ppi_map('corrected_reflectivity', sweep=0, vmin=0, vmax=65,
                     colorbar_label='[dBZ]', mask_outside=True, ax=ax,
                     min_lat=lat0, max_lat=lat1, min_lon=lon0, max_lon=lon1,
                     lon_lines=lon_lines, lat_lines=lat_lines, zorder=0, cmap='pyart_NWSRef')

#plota os aneis de distancia
display.plot_range_rings([50,100,150,200,250], lw=0.5)

plt.tight_layout()
plt.show()
