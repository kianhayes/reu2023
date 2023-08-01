import yt
import os
import unyt
from yt.units import dimensions
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
from yt.visualization.volume_rendering.api import Scene, create_volume_source, Camera, ColorTransferFunction
import numpy as np

yt.enable_parallelism()

ds = yt.load('/gpfs/projects/CalderGroup/BrendanSpace/SIM_DATA/hires_urca_problem/plt0030084')

def _Ye(field, data):
    # sum 1/2 
    Ye=0.5*(data['boxlib', 'X(c12)']+data['boxlib', 'X(o16)']+data['boxlib', 'X(he4)']+data['boxlib', 'X(ne20)'])
    
    #sum ones
    Ye+=(data['boxlib', 'X(h1)'])
    
    #A=23 nucleons
    Ye+= (10.*data['boxlib', 'X(ne23)'] + 11.*data['boxlib', 'X(na23)'] + 12.*data['boxlib', 'X(mg23)'])/23.
    
    return Ye

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
sc = Scene()

# Setting the radius of the sphere that's rendered
radius = (1.8e3, 'km')

# Setting up the data to render as the Source part of the Scene (sc)
core = ds.sphere(ds.domain_center, (500, 'km'))
my_source = create_volume_source(core, field)
my_source.set_log(False)

nlayers = 8
### Transfer Function (Coloring)
bounds = (2.8e-5, 3.5e-5) # These are the bounds for 
# setup our transfer function
tfh = TransferFunctionHelper(ds) # this object helps with some of the syntax
tfh.set_field(field) # set what field we are looking at. Should match the source.
tfh.set_log(False) # volume rendering generally looks best in logspace
tfh.grey_opacity = True
tfh.set_bounds(bounds) 
tfh.build_transfer_function()

#tfh.tf.add_layers(
    #nlayers,
    #w=0.01,
    #mi=bounds[0], # Sets the min x limit
    #ma=bounds[1], # Sets the max x limit
    #col_bounds=[-15, -8], # This changes the area of the color map that will be used
    #alpha=np.logspace(-1, 6, 20), # Changes the y-axis TransferFunction plot (how high the alpha value is)
    #colormap='twilight', # Changes the color map
#)


tfh.tf.map_to_colormap(bounds[0], bounds[1], colormap="twilight")

my_source.transfer_function = tfh.tf

### Camera
#Adding source to scene
sc.add_source(my_source)

# Add a camera to scene
sc.add_camera(ds, lens_type="perspective")

# Set camera properties
sc.camera.focus = ds.domain_center #point cam to center
sc.camera.resolution = 1000 #set the resolution
sc.camera.north_vector = unyt.unyt_array([0., 1., 0.], 'km') # set "up" to be y-direction. Note size doesn't matter.

# set the physical position of the camera. 
# Want to be far enough from center that we see the whole Source.
sc.camera.position = ds.domain_center + unyt.unyt_array([0., 0., 0.80*radius[0]], 'km') # moving 3x away along z-direction
sc.camera.set_width(radius)

sc.annotate_axes(alpha=0.001)

# Rotate around the object and render an image
for i in sc.camera.iter_rotate(2*np.pi, 36, rot_center=ds.domain_center):
    sc.render()

    if yt.is_root():
        sc.save(f'/gpfs/projects/CalderGroup/KianSpace/plots/urca/3d_renders/rotate/ye_sub/images/3d_render_{field[1]}_rot{i}.png', render=False, sigma_clip=2)







