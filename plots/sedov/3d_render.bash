#!/bin/bash
#SBATCH --job-name=3d-render
#SBATCH --output=output_hybrid.txt
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=28
#SBATCH --time=4:00:00
#SBATCH -p short-28core
#SBATCH --mail-type=ALL
#SBATCH --mail-user=kian.hayes@stonybrook.edu

module purge
module load anaconda
call source activate yt

RUN_DIR=/gpfs/projects/CalderGroup/KianSpace/reu2023/plots/sedov
LOGFILE=$RUN_DIR/3d_render.log

cd $RUN_DIR
echo 'Start of 3D Render', $(date) >> $LOGFILE
mpirun ./3d_render.py >> $LOGFILE
echo 'End of 3D Render', $(date) >> $LOGFILE