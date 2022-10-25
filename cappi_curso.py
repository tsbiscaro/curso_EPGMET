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



# Cria CAPPI e plota
import numpy as np
import matplotlib.pyplot as plt
import pyart
import cartopy.crs as ccrs
import geopy
from geopy import distance

radar = pyart.aux_io.read_gamic('JG1-20220816234803.HDF5')

#cantos da imagem
#tamanho da imagem - 5 x 5 graus (aprox. um raio de 250 km)
sz = 5.0

lat0 = radar.latitude['data'][0] - sz/2
lat1 = radar.latitude['data'][0] + sz/2
lon0 = radar.longitude['data'][0] - sz/2
lon1 = radar.longitude['data'][0] + sz/2

lat_radar, lon_radar = radar.latitude['data'][0], radar.longitude['data'][0]

#3 grid lines com o centro no radar
dl = sz/5
lon_lines=np.arange(lon0, lon1, dl)
lat_lines=np.arange(lat0, lat1, dl)


fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())


#cria um cappi de 500 x 500 pontos, com 250 km de raio
#3 niveis, de 2 a 4 km, com 1 km de intervalo
cappi = pyart.map.grid_from_radars(radar, grid_shape=(3, 500, 500),
                                   grid_limits=((2000, 4000,),
                                                (-250000., 250000.),
                                                (-250000, 250000.)),
                                   grid_origin = (lat_radar, lon_radar),
                                   gridding_algo='map_gates_to_grid',
                                   roi_func='dist_beam', min_radius=2000.0,
                                   weighting_function='Nearest')

display = pyart.graph.GridMapDisplay(cappi)
#level 0 = 2km, level 1 = 3km, etc...
display.plot_grid("corrected_reflectivity", level=1, vmin=0, vmax=65,
                  ax=ax, colorbar_label='[dBZ]', mask_outside=True, cmap='pyart_NWSRef')


ax.set_xlabel('')
ax.set_ylabel('')

# Plota os aneis de distancia do radar
plota_aneis([50,100,150,200,250], lon_radar, lat_radar, 'grey', label='')

plt.show()
plt.tight_layout()


