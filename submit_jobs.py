#!/bin/bash

for i in $(seq -w 001 552)
do
    dir_name="main_dir_$i"
    cd $dir_name
    sbatch job.sh
    cd ..
done
