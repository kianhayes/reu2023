import yt
import os
import unyt
from yt.units import dimensions
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
from yt.visualization.volume_rendering.api import Scene, create_volume_source, Camera, ColorTransferFunction
import numpy as np
#from yt.utilities.parallel_tools.parallel_analysis_interface import Communicator

yt.enable_parallelism()

path = '/gpfs/projects/CalderGroup/KianSpace/sedov_runs/results2'
os.chdir(path)

field = ('flash', 'temp')

data_series = yt.load('sedov_hdf5_plt_cnt_*')

for ds in data_series.piter():
    sc = Scene()

    # Setting the radius of the sphere that's rendered
    radius = 0.5

    # Setting up the data to render as the Source part of the Scene (sc)
    core = ds.sphere(ds.domain_center, (radius, 'mm'))
    my_source = create_volume_source(core, field)

    ### Transfer Function (Coloring)
    bounds = (1e-5, 5e-4)
    # setup our transfer function
    tfh = TransferFunctionHelper(ds) # this object helps with some of the syntax
    tfh.set_field(field) # set what field we are looking at. Should match the source.
    tfh.set_log(True) # volume rendering generally looks best in logspace
    tfh.grey_opacity = False
    tfh.set_bounds(bounds) 
    tfh.build_transfer_function() # this generates a blank transfer function that we can add gaussians to.

    tfh.tf.map_to_colormap(np.log10(bounds[0]), np.log10(bounds[1]), colormap="inferno")

    my_source.transfer_function = tfh.tf

    ### Camera
    #Adding source to scene
    sc.add_source(my_source)

    # Add a camera to scene
    sc.add_camera(ds, lens_type="perspective")

    # Set camera properties
    sc.camera.focus = ds.domain_center #point cam to center
    sc.camera.resolution = 1080 #set the resolution
    sc.camera.north_vector = unyt.unyt_array([0., 1., 0.], 'mm') # set "up" to be y-direction. Note size doesn't matter.

    # set the physical position of the camera. 
    # Want to be far enough from center that we see the whole Source.
    sc.camera.position = ds.domain_center + unyt.unyt_array([0., 0., 1], 'mm') # moving 3x away along z-direction
    sc.camera.set_width((radius, 'mm'))

    sc.render()

    if yt.is_root():
        sc.save(f'/gpfs/projects/CalderGroup/KianSpace/reu2023/plots/sedov/june-29/3d-images/{ds}_3d_render', render=False)
