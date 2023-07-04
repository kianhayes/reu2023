import yt
import os

yt.enable_parallelism

ds = yt.load('/gpfs/projects/CalderGroup/run_for_kian/hdef_hdf5_plt_cnt_*')

field = ('flash', 'temp')

for ds in ds.piter():
    slc = yt.SlicePlot(ds, 'theta', field)
    #No methods like set_xlim, can only zoom, pan, and re-center
    z = 10.0  #Set a zoom factor
    slc.zoom(z)   #Zooms in around the center of the plot (change center with p.set_center())

    #But all the action is at (0.0, 0.0), so we want this to be the left-most center point. That means we need to pan over
    pr_x = -0.5*z + 0.5 #Pan over to the left, if zoom is 1 then no panning
    pr_y = 0.0          #Stay centered in y
    slc.pan_rel((pr_x, pr_y))
    slc.set_cmap(field, 'inferno')
    if yt.is_root():
        slc.save('/gpfs/projects/CalderGroup/KianSpace/reu2023/plots/snia/july-3/temperature/', render=False)