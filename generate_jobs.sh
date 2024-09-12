#!/bin/bash

for i in $(seq -w 001 552)
do
    dir_name="main_dir_$i"
    mkdir -p $dir_name
    sed "s/main_dir_XX/main_dir_$i/g" job_template.sh > $dir_name/job.sh
    cp run_psi4.py $dir_name/
done
