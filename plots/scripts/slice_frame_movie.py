import yt
import os

yt.enable_parallelism()

dataset = yt.load('/gpfs/projects/CalderGroup/KianSpace/snia_hddt_runs/july-3-results/hdef_hdf5_plt_cnt_*')

field = ('boxlib', 'rhoX(na23)')

for ds in dataset.piter():
    slc = yt.SlicePlot(ds, 'z', field)
    z = 5 #Set a zoom factor
    slc.zoom(z) #Zooms in around the center of the plot (change center with p.set_center())

    #But all the action is at (0.0, 0.0), so we want this to be the left-most center point. That means we need to pan over
    pr_x = -0.5*z + 0.5 #Pan over to the left, if zoom is 1 then no panning
    pr_y = 0.0          #Stay centered in y
    slc.pan_rel((pr_x, pr_y))
    slc.set_cmap(field, 'twilight')
    slc.set_log(field, linthresh=(10**2))
    slc.hide_axes()
    slc.hide_colorbar()

    if yt.is_root():
        slc.save('/gpfs/projects/CalderGroup/KianSpace/reu2023/plots/snia/july-5/phfa/images/')