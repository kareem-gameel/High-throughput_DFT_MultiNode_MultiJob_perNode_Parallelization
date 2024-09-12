#!/bin/bash

# SLURM submission script for multiple serial jobs on Niagara
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2  # 2 tasks for 2 files
#SBATCH --cpus-per-task=20    # Each task uses 20 CPUs
#SBATCH --time=12:00:00       # Set a time limit for debugging
#SBATCH --job-name=main_dir_XX
#SBATCH --output=job_output_%j.txt
#SBATCH --error=job_error_%j.txt

# Allow hyperthreading so each task uses 40 effective threads
export OMP_NUM_THREADS=40

# Load the required modules
module load CCEnv
module load StdEnv/2020
module load intel/2020
module load openmpi
module load psi4/1.5

source ~/xtb_env/bin/activate

# EXECUTION COMMAND
parallel --joblog slurm-$SLURM_JOBID.log -j $SLURM_TASKS_PER_NODE "
    subdir=subdir_{};
    tmpdir=\${SLURM_SUBMIT_DIR}/\${subdir}/tmp;
    mkdir -p \$tmpdir;
    if [ -d \$tmpdir ]; then
        export PSI_SCRATCH=\$tmpdir;
        cd \$subdir && python ../run_psi4.py file_{}.xyz;
    else
        echo 'Failed to create directory \$tmpdir' >&2;
        exit 1;
    fi
" ::: $(seq -w 01 02)

# Clean up the temporary directories after the job is done
parallel --joblog slurm-$SLURM_JOBID.log -j $SLURM_TASKS_PER_NODE "rm -rf subdir_{}/tmp" ::: $(seq -w 01 02)
