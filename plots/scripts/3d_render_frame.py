import yt
import os
import unyt
from yt.units import dimensions
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
from yt.visualization.volume_rendering.api import Scene, create_volume_source, Camera, ColorTransferFunction
import numpy as np

yt.enable_parallelism()

ds = yt.load('/gpfs/projects/CalderGroup/BrendanSpace/SIM_DATA/hires_urca_problem/plt0030084')
field = ('boxlib', 'rhoX(na23)')
sc = Scene()

# Setting the radius of the sphere that's rendered
radius = (1.8e3, 'km')

# Setting up the data to render as the Source part of the Scene (sc)
core = ds.sphere(ds.domain_center, radius)
my_source = create_volume_source(core, field)

### Transfer Function (Coloring)
bounds = (2e5, 4e5) # These are the bounds for 
# setup our transfer function
tfh = TransferFunctionHelper(ds) # this object helps with some of the syntax
tfh.set_field(field) # set what field we are looking at. Should match the source.
tfh.set_log(True) # volume rendering generally looks best in logspace
tfh.grey_opacity = False
tfh.set_bounds(bounds)
tfh.build_transfer_function() # this generates a blank transfer function

#tfh.tf.add_layers(
    #nlayers,
    #w=0.01,
    #mi=np.log10(bounds[0]), # Sets the min x limit
    #ma=np.log10(bounds[1]), # Sets the max x limit
    #col_bounds=[-15, -8], # This changes the area of the color map that will be used
    #alpha=np.logspace(-1, 6, 20), # Changes the y-axis TransferFunction plot (how high the alpha value is)
    #colormap='inferno', # Changes the color map
#)

tfh.tf.map_to_colormap(np.log10(bounds[0]), np.log10(bounds[1]), colormap="twilight", scale=1e-1)

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

sc.render()
if yt.is_root():
    sc.save(f'/gpfs/projects/CalderGroup/KianSpace/reu2023/plots/urca/3d_render_{field[1]}', render=False, sigma_clip=2)
