#plota um corte vertical em um volume
import matplotlib.pyplot as plt
import pyart

radar = pyart.aux_io.read_gamic('JG1-20220816234803.HDF5')
rhi = pyart.util.cross_section_ppi(radar, [20, 240])
display = pyart.graph.RadarDisplay(rhi)

fig = plt.figure(figsize=(10,8))

fig.add_subplot(211)
display.plot('reflectivity', 0, vmin=0, vmax=65, 
             cmap='pyart_NWSRef', colorbar_label='[dBZ]')
display.set_limits(ylim=[0,15], xlim=[0,250])

fig.add_subplot(212)
display.plot('reflectivity', 1, vmin=0, vmax=65, 
             cmap='pyart_NWSRef', colorbar_label='[dBZ]')
display.set_limits(ylim=[0,15], xlim=[0,250])

plt.show()
plt.tight_layout()
