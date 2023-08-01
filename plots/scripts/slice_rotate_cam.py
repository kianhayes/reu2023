import yt
import os
import numpy as np

yt.enable_parallelism()

# Calculation of the Ye field
def _Ye(field, data):
    # sum 1/2 
    Ye=0.5*(data['boxlib', 'X(c12)']+data['boxlib', 'X(o16)']+data['boxlib', 'X(he4)']+data['boxlib', 'X(ne20)'])
    
    #sum ones
    Ye+=(data['boxlib', 'X(h1)'])
    
    #A=23 nucleons
    Ye+= (10.*data['boxlib', 'X(ne23)'] + 11.*data['boxlib', 'X(na23)'] + 12.*data['boxlib', 'X(mg23)'])/23.
    
    return Ye

ds = yt.load('/gpfs/projects/CalderGroup/BrendanSpace/SIM_DATA/hires_urca_problem/plt0030084')

ds.add_field(name=("boxlib", "Ye"),
             function=_Ye,
             take_log=True,
             units = "dimensionless",
             sampling_type="local")

def _Ye_sub(field, data):
    Ye_sub = (0.5 - data['boxlib', 'Ye'])

    return Ye_sub

ds.add_field(name=("boxlib", "Ye_sub"),
             function=_Ye_sub,
             take_log=True,
             units = "dimensionless",
             sampling_type="local")

field = ('boxlib', 'Ye_sub')
    
thetas = np.linspace(0, 2*np.pi, 60)

normal_direction = 'y'

# Get what element theta is in the theta list
for theta in thetas:

    # Setting up file name
    for i in range(len(thetas)):
        if theta == thetas[i]:
            filename = f'{normal_direction}_{field[1]}_rot{i+1}.png'
        else:
            continue

    z_vector = round(np.cos(theta), 2)
    x_vector = round(np.sin(theta), 2)
    degrees = theta * (180/np.pi)

    slc = yt.OffAxisSlicePlot(ds, normal=(0, z_vector, x_vector), fields=field, north_vector=(1,0,0), center=ds.domain_center, width=(1000, 'km'))
    z = 5 #Set a zoom factor
    #slc.zoom(z) #Zooms in around the center of the plot (change center with p.set_center())
    slc.set_cmap(field, 'twilight_shifted')
    slc.set_log(field, False)
    slc.set_zlim(field, zmin=3e-5, zmax=3.35e-5)
    slc.annotate_contour(('boxlib', 'rho'), levels=1, factor=1, clim=(1.9e9, 1.9e9))
    slc.set_colorbar_label(field, '')
    slc.hide_axes()
    slc.set_colorbar_minorticks(field, False)
    slc.annotate_title(f'Angle Rotated Around Source (degrees): {round(degrees, 2)}')
    slc.set_font_size(18)
    
    if yt.is_root():
        slc.save(f'/gpfs/projects/CalderGroup/KianSpace/plots/urca/slices/rotate/ye/images/{filename}')