
# High-Throughput DFT Pipeline

This repository contains a high-throughput DFT (Density Functional Theory) pipeline using Psi4 for quantum chemistry calculations. The pipeline is designed for parallelized execution on the Niagara cluster using SLURM for job scheduling.

## Overview

The pipeline is built around the following main components:
1. **XYZ File Splitting**: Large XYZ files containing multiple molecular geometries are split into smaller files using the `split_xyz.py` script.
2. **SLURM Job Submission**: A template SLURM script (`job_template.sh`) is used to submit jobs to the Niagara compute cluster for parallel execution of Psi4 calculations.
3. **Psi4 Execution**: For each molecule, a Psi4 input file is generated and the energy calculation is performed using the `run_psi4.py` script.
4. **Result Compilation**: The energies and calculation times for all molecules are stored in output CSV files, and temporary directories are cleaned up after the calculations.

## Pipeline Structure

1. **Splitting XYZ Files**
   The `split_xyz.py` script reads a large XYZ file containing multiple molecules, and splits it into smaller XYZ files across several directories for parallel processing. Each main directory contains subdirectories where the individual files are placed.

   Example usage:
   ```bash
   python split_xyz.py <input_xyz_file> <num_main_dirs> <num_subdirs>
   ```

2. **Job Generation**
   The `generate_jobs.sh` script is used to automatically generate job submission scripts for each main directory based on the provided template (`job_template.sh`). The job scripts are placed in the corresponding main directories.

   Example usage:
   ```bash
   ./generate_jobs.sh
   ```

3. **Psi4 Execution**
   The `run_psi4.py` script generates Psi4 input files for each molecule, runs Psi4 energy calculations, and writes the results (energy and calculation time) to CSV files. It checks if a molecule has already been processed and skips it if necessary.

   Example usage:
   ```bash
   python run_psi4.py <xyz_file>
   ```

4. **Job Submission**
   The `submit_jobs.sh` script submits all the generated job scripts to the SLURM scheduler for execution on the Niagara cluster.

   Example usage:
   ```bash
   ./submit_jobs.sh
   ```

## Directory Structure

- `main_dir_XXX/` - Main directories containing subdirectories for individual molecule files.
- `subdir_XX/` - Subdirectories containing individual XYZ files for each molecule.
- `job_template.sh` - Template SLURM script for running Psi4 calculations.
- `generate_jobs.sh` - Script to generate job submission scripts for each main directory.
- `run_psi4.py` - Script to generate Psi4 input files, run calculations, and store results.
- `submit_jobs.sh` - Script to submit all job scripts to the SLURM scheduler.

## File Descriptions

- **split_xyz.py**: Splits a large XYZ file into smaller files for parallel processing.
- **job_template.sh**: Template SLURM script for running Psi4 jobs with 2 tasks and 20 CPUs per task.
- **generate_jobs.sh**: Generates job scripts for each main directory.
- **run_psi4.py**: Runs Psi4 calculations for molecules, saves energies, and cleans up temporary files.
- **submit_jobs.sh**: Submits job scripts to the SLURM scheduler for execution.

## Requirements

- Psi4
- SLURM
- Python 3
- Niagara Compute Cluster

## Usage

1. Split the large XYZ file into smaller files using `split_xyz.py`.
2. Generate job scripts using `generate_jobs.sh`.
3. Submit the jobs to the SLURM scheduler using `submit_jobs.sh`.
4. Monitor the job outputs and compile the results once the jobs are finished.

## Example Workflow

```bash
# Step 1: Split the dataset
python split_xyz.py tmqm_co_diss_xtb_opt_remainder.xyz 552 2

# Step 2: Generate job scripts
./generate_jobs.sh

# Step 3: Submit the jobs to the scheduler
./submit_jobs.sh
```

## License
This project is licensed under the MIT License.
