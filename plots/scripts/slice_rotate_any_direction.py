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

field = ('boxlib', 'Ye')

def slice_rotate(normal_vector, steps):
    directions = ['x', 'y', 'z', 'all']
    xs = []
    ys = []
    zs = []

    # Check if given normal_vector is in the directions list
    if normal_vector not in directions:
        raise TypeError('Given normal vector is invalid')

    # Give the correct vector based on the given normal vector
    if normal_vector == 'x':
        
    thetas = np.linspace(0, 2*np.pi, steps)

    # Get what element theta is in the theta list
    for theta in thetas:

        # Setting up file name
        for i in range(len(thetas)):
            if theta == thetas[i]:
                filename = f'{normal_vector}_{field[1]}_rot{i+1}.png'
            else:
                continue

        z_vector = round(np.cos(theta), 2)
        x_vector = round(np.sin(theta), 2)

        slc = yt.OffAxisSlicePlot(ds, normal=(x_vector, 0, z_vector), fields=field, north_vector=(0,1,0), center=ds.domain_center)
        z = 5 #Set a zoom factor
        slc.zoom(z) #Zooms in around the center of the plot (change center with p.set_center())
        slc.set_cmap(field, 'twilight')
        #slc.set_log(field)
        slc.annotate_title(f'z={z_vector}, x={x_vector}, theta={theta}')
        
        if yt.is_root():
            slc.save(f'/gpfs/projects/CalderGroup/KianSpace/plots/urca/slices/rotate/ye/images/{filename}')


