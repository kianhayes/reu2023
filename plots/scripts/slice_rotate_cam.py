import yt
import os
import numpy as np

yt.enable_parallelism()

ds = yt.load('/gpfs/projects/CalderGroup/BrendanSpace/SIM_DATA/hires_urca_problem/plt0030084')

field = ('boxlib', 'rhoX(na23)')
thetas = np.linspace(0, 2*np.pi, 60)

# Get what element theta is in the theta list
for theta in thetas:

    # Setting up file name
    for i in range(len(thetas)):
        if theta == thetas[i]:
            filename = f'{field[1]}_rot{i+1}.png'
        else:
            continue

    z_vector = round(np.cos(theta), 2)
    x_vector = round(np.sin(theta), 2)
    slc = yt.OffAxisSlicePlot(ds, normal=(x_vector, 0, z_vector), fields=field, north_vector=(0,1,0), center=ds.domain_center)
    z = 5 # Set a zoom factor
    slc.zoom(z) # Zooms in around the center of the plot (change center with p.set_center())
    slc.set_cmap(field, 'twilight')
    slc.set_log(field, False)
    slc.set_zlim(field, zmin=2e5, zmax=1e5)
    slc.annotate_contour(('boxlib', 'rho'), levels=1, factor=1, clim=(1.9e9, 1.9e9))

    degrees = round(theta * (180/np.pi))

    slc.annotate_title(f'z={z_vector}, x={x_vector}, theta={degrees}')
    
    if yt.is_root():
        slc.save(f'/gpfs/projects/CalderGroup/KianSpace/plots/urca/slices/rotate/rhoX(na23)/images/{filename}')