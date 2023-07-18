import yt
from yt.visualization.volume_rendering.api import Scene, create_volume_source
import unyt
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
import numpy as np

yt.enable_parallelism()

ds = yt.load('/gpfs/projects/CalderGroup/BrendanSpace/SIM_DATA/hires_urca_problem/plt0030084')
ds.force_periodicity()
field1 = ('boxlib', 'X(na23)')
field2 = ('boxlib', 'X(c12)')
sc = Scene()

radius = (1.8e3, 'km')

core = ds.sphere(ds.domain_center, radius)
volume1 = create_volume_source(core, field1)
volume2 = create_volume_source(core, field2)

bounds = (1e6, 5e6) # These are the bounds for the transfer function
tfh = TransferFunctionHelper(ds)
tfh.set_log(True) # volume rendering generally looks best in logspace
tfh.grey_opacity = False
tfh.set_bounds(bounds)
tfh.build_transfer_function() # this generates a blank transfer function
# set up camera

tfh.tf.map_to_colormap(np.log10(bounds[0]), np.log10(bounds[1]), colormap="twilight")

volume1.transfer_function = tfh.tf
volume2.transfer_function = tfh.tf

sc.add_source(volume1)
sc.add_source(volume2)

sc.add_camera(ds, lens_type="perspective")
sc.camera.focus = ds.domain_center
sc.camera.resolution = 400
sc.camera.north_vector = unyt.unyt_array([0., 1., 0.], 'km')
sc.camera.position = ds.domain_center + unyt.unyt_array([0., 0., 0.80*radius[0]], 'km')
sc.camera.set_width(radius)

sc.render()
if yt.is_root():
    sc.save(f"/gpfs/projects/CalderGroup/KianSpace/reu2023/plots/urca/{field1[1]}_{field2[1]}_3d_render", render=False, sigma_clip=2)