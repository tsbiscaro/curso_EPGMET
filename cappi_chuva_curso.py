#----------------------------------------------------------------------------------- 
#  Funcao que plota circulos de distancia em geral 
#----------------------------------------------------------------------------------- 
def plota_aneis(aneis, lon_r, lat_r, color, label):
#fonte: Prof. Enrique Mattos - UNIFEI
    """
    """

    origin = geopy.Point(lat_r, lon_r)

    lons = np.zeros((len(aneis), 361))
    lats = np.zeros((len(aneis), 361))
    for i, dis in enumerate(aneis):
        xpts = []
        ypts = []
        for az in range(361): 
            destination = distance.distance(kilometers=dis).destination(origin, az)
            lat2, lon2 = destination.latitude, destination.longitude
            xpts.append(lon2)
            ypts.append(lat2)
        lons[i,:] = xpts[:]
        lats[i,:] = ypts[:]   

    for i, anel in enumerate(aneis):
        ax.plot(lons[i,:], lats[i,:], color=color, label= label)

#Cria um cappi de chuva
import numpy as np
import matplotlib.pyplot as plt
import pyart
import cartopy.crs as ccrs
import geopy
from geopy import distance


radar = pyart.aux_io.read_gamic('JG1-20220816234803.HDF5')
lat_radar, lon_radar = radar.latitude['data'][0], radar.longitude['data'][0]

#calcula as estimativas de precipitacao atraves de 3 metodos diferentes
chuva_zr = pyart.retrieve.est_rain_rate_z(radar, refl_field='corrected_reflectivity')
chuva_zdp = pyart.retrieve.est_rain_rate_zkdp(radar, refl_field='corrected_reflectivity', thresh_max=True, thresh=40)
chuva_dp = pyart.retrieve.est_rain_rate_kdp(radar, kdp_field='specific_differential_phase')

#adiciona os campos criados na estrutura radar
radar.add_field('chuva_zr', chuva_zr)
radar.add_field('chuva_dp', chuva_dp)
radar.add_field('chuva_zdp', chuva_zdp)

cappi = pyart.map.grid_from_radars(radar, grid_shape=(1, 500, 500),
                                   grid_limits=((3000, 3000,),
                                                (-250000., 250000.),
                                                (-250000, 250000.)),
                                   grid_origin = (lat_radar, lon_radar),
                                   gridding_algo='map_gates_to_grid',
                                   roi_func='dist_beam', min_radius=2000.0,
                                   weighting_function='Nearest')


fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

display = pyart.graph.GridMapDisplay(cappi)
display.plot_grid("chuva_zdp", level=0, vmin=0, vmax=100, cmap='pyart_LangRainbow12',
                  ax=ax, colorbar_label='[mm/h]', mask_outside=False)


ax.set_xlabel('')
ax.set_ylabel('')

# Plota os aneis de distancia do radar
plota_aneis([50,100,150,200,250], lon_radar, lat_radar, 'grey', label='')

plt.show()
plt.tight_layout()


