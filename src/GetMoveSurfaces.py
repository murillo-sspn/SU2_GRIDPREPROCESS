#!/usr/bin/env python3
import sys, os, shutil
from subprocess import Popen, run
import copy
from mpi4py.MPI import COMM_SELF as MPI_COMM, Info

def main(SU2_config_original_file, surfaces, su2_version):

    output_dir = "./output"

    # Add './' if not in the original config file
    if not("./" == SU2_config_original_file[0:1]):
        SU2_config_original_file = "./" + SU2_config_original_file

    # Modified cfg file
    SU2_config_modified_file = SU2_config_original_file.replace(".cfg","_MoveSurface.cfg")

    # Open original SU2 config file
    f = open(SU2_config_original_file,"r")
    SU2_config_original = f.read()
    f.close()

    # Get mesh info
    MESH_FILENAME       = get_config_info(config = SU2_config_original, option="MESH_FILENAME")
    MESH_OUT_FILENAME   = get_config_info(config=SU2_config_original, option="MESH_OUT_FILENAME")

    # Current directory
    w_dir = os.curdir

    # Remove old files
    if os.path.exists(output_dir):
        os.system("rm -rf " + output_dir)
    for file in os.listdir(w_dir):
        if ".dat" in file or ".txt" in file or ".stl" in file:
            os.remove(file)
    if os.path.exists(SU2_config_modified_file):
        os.remove(SU2_config_modified_file)

    # Make output folder
    os.mkdir(output_dir)

    for surface in surfaces:
        print(f"surface = {surface}")

        # Delete old modified config file
        if os.path.exists(SU2_config_modified_file):
            os.remove(SU2_config_modified_file)

        # Update modified config file
        SU2_config_modified = copy.deepcopy(SU2_config_original)

        SU2_config_modified=SU2_config_modified.replace("DV_MARKER= ( )",
                                                        f"DV_MARKER= ( {surface} )")

        if su2_version == 5:
            SU2_config_modified = SU2_config_modified.replace("MARKER_MOVING= ( )",
                                                              f"MARKER_MOVING= ( {surface} )")
            motion_filename = "MOTION_FILENAME"

        elif su2_version == 8:
            motion_filename = "DV_FILENAME"

        SU2_config_modified = SU2_config_modified.replace(f"{motion_filename}= MoveSurface.txt",
                                                          f"{motion_filename}= MoveSurface{surface.capitalize()}.txt")

        # Write modified config file
        f = open(SU2_config_modified_file, "w")
        f.write(SU2_config_modified)
        f.close()

        # Run 'SU2_DEF' to extract the MoveSurface file
        SU2_run(SU2_executable="SU2_DEF", cfg_file_name=SU2_config_modified_file)

    for file in os.listdir(w_dir):
        # Move the MoveSurface files to the outputs directory
        if ".txt" in file:
            shutil.move(file,output_dir+"/"+file)
        # Remove irrelevant files for the MoveSurface generation
        if ".dat" in file or ".stl" in file:
            os.remove(file)

    if os.path.exists(MESH_OUT_FILENAME):
        # Remove output mesh
        os.remove(MESH_OUT_FILENAME)

    if os.path.exists(SU2_config_modified_file):
        # Remove modified .cfg file
        os.remove(SU2_config_modified_file)

def get_config_info(config, option):
    index0 = config.find(option)
    index1 = config.find('=',index0)
    index2 = config.find('\n',index1)
    info = config[index1:index2].replace(' ','').replace('=','').replace('\n','')
    return info

def SU2_run(SU2_executable, cfg_file_name):

    SU2_executable = os.path.join(os.environ["SU2_RUN"], SU2_executable)

    command = f'{SU2_executable} {cfg_file_name}'
    print(f"\n{command}\n")

    # Submit command
    p = Popen(
            command,
            shell=True,
            stderr=sys.stderr,
            env=os.environ,
        )

    # Wait until the process is finished to continue
    #   Check https://stackoverflow.com/questions/2837214/python-popen-command-wait-until-the-command-is-finished
    p.communicate()

    # MPI_COMM.Spawn(
    #     SU2_executable,
    #     args=[cfg_file_name],
    #     maxprocs=1,
    # )

    # run([f'{SU2_executable} {cfg_file_name}'])

# Call 'GetMoveSurfaces.py' from the terminal using two arguments:
#   1) SU2 config file:
#           Example: config_CFD.cfg
#   2) List of surfaces to be matched:
#           Example: ["BLADE","HUB","SHROUD","INFLOW","OUTFLOW","PER1","PER2"]
#   3) Say SU2 version, either 5 or 8
if __name__ == "__main__":
    # SU2 config file
    cfg_file = sys.argv[1]
    # List of surfaces that will be extracted in MoveSurface files
    surfaces = sys.argv[2]
    # List of surfaces that will be extracted in MoveSurface files
    su2_version = int(sys.argv[3])
    # Convert string into a list
    surfaces=(surfaces
              .replace('[','')
              .replace(']','')
              .split(','))
    # The surfaces list looks like this:
        # surfaces = ["BLADE","HUB","SHROUD","INFLOW","OUTFLOW","PER1","PER2"]
    main(cfg_file, surfaces, su2_version)
