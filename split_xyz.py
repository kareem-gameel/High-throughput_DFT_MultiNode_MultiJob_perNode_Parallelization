import os
import shutil

def split_dataset(input_file, num_main_dirs=552, num_subdirs=2):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    molecules = []
    current_molecule = []
    for line in lines:
        current_molecule.append(line)
        if len(current_molecule) == int(current_molecule[0].strip()) + 2:
            molecules.append(current_molecule)
            current_molecule = []
    
    total_molecules = len(molecules)
    molecules_per_subdir = total_molecules // (num_main_dirs * num_subdirs)
    extra_molecules = total_molecules % (num_main_dirs * num_subdirs)
    
    molecule_index = 0
    for main_dir_count in range(1, num_main_dirs + 1):
        main_dir = f"main_dir_{main_dir_count:03d}"
        if os.path.exists(main_dir):
            # Remove all existing subdirectories within the main_dir
            for subdir in os.listdir(main_dir):
                subdir_path = os.path.join(main_dir, subdir)
                if os.path.isdir(subdir_path):
                    shutil.rmtree(subdir_path)
        
        os.makedirs(main_dir, exist_ok=True)
        
        for subdir_count in range(1, num_subdirs + 1):
            subdir = f"{main_dir}/subdir_{subdir_count:02d}"
            os.makedirs(subdir, exist_ok=True)
            
            num_molecules_in_file = molecules_per_subdir
            if extra_molecules > 0:
                num_molecules_in_file += 1
                extra_molecules -= 1
            
            subdir_file = f"{subdir}/file_{subdir_count:02d}.xyz"
            with open(subdir_file, 'w') as subfile:
                for _ in range(num_molecules_in_file):
                    if molecule_index < total_molecules:
                        subfile.writelines(molecules[molecule_index])
                        molecule_index += 1
                    else:
                        break

            if molecule_index >= total_molecules:
                break
        if molecule_index >= total_molecules:
            break

input_file = 'tmqm_co_diss_xtb_opt.xyz'
split_dataset(input_file, num_main_dirs=552, num_subdirs=2)
