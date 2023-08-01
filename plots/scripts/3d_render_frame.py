import yt
import os
import unyt
from yt.units import dimensions
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
from yt.visualization.volume_rendering.api import Scene, create_volume_source, Camera, ColorTransferFunction
import numpy as np

yt.enable_parallelism()

ds = yt.load('/gpfs/projects/CalderGroup/BrendanSpace/SIM_DATA/hires_urca_problem/plt0030084')
field = ('boxlib', 'X(ne23)')
sc = Scene()

# Setting the radius of the sphere that's rendered
radius = (1.8e3, 'km')

# Setting up the data to render as the Source part of the Scene (sc)
core = ds.sphere(ds.domain_center, radius)
my_source = create_volume_source(core, field)
so_urca = create_volume_source(core, ('boxlib', 'rho'))
my_source.set_log(False)

### Transfer Function (Coloring)
bounds = (4.5e-4, 6e-4) # These are the bounds for 
# setup our transfer function
tfh = TransferFunctionHelper(ds) # this object helps with some of the syntax
tfh.set_field(field) # set what field we are looking at. Should match the source.
tfh.set_log(False) # volume rendering generally looks best in logspace
tfh.grey_opacity = False
tfh.set_bounds(bounds)
tfh.build_transfer_function()
tfh.tf.map_to_colormap(bounds[0], bounds[1], colormap="twilight")

my_source.transfer_function = tfh.tf
sc.add_source(my_source)

# create transfer function
tfh.set_field(('boxlib', 'rho'))
tfh.set_log(True)
tfh.grey_opacity = False
tfh.set_bounds((1.e9, 4.5e9))
tfh.build_transfer_function()
# add gaussian at 1.9e9 g/cm^3 with width 0.005^2
tfh.tf.add_gaussian(np.log10(1.9e9), (0.005)**2, [1., 1., 0.21, 1]) # should give a yellowish thing

#add transfer func to source
so_urca.transfer_function = tfh.tf

# add source to scene
sc.add_source(so_urca)

### Camera
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
    sc.save(f'/gpfs/projects/CalderGroup/KianSpace/reu2023/plots/urca/3d_renders/frames/3d_render_{field[1]}.png', render=False, sigma_clip=2)
