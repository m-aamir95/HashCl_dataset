import os
import subprocess   
import time

# Points to the root path of the polybench-benchmark applications against which we are going to generate the dataset
# The dataset will contain multiple versions of same polybench kernels apps with variable data size
# Executed on the CPU and GPU seperatly for execution time comparisons
POLYBENCH_APPS_ROOT_PATH = "./POLYBENCH_KERNELS/linear-algebra/kernels"

POLYBENCH_APPS_ROOT_PATH_GPU = "./POLYBENCH_KERNELS/linear-algebra/GPU_kernels"

# Target directories folder structure
"""
    Generated_Dataset
            |
            --- CPU_APPS    (Kernels will be configured to use the INTEL SDK)
            |    |
            |    --- MINI_VVSMALL_Dataset_Apps
            |    |
                 --- MINI_VSMALL_Dataset_Apps 
                 |
                 --- MINI_SMALL_Dataset_Apps    
                 |
            |    --- MINI_Dataset_Apps
            |    |   
            |    --- Small_Dataset_Apps
            |    |
            |    --- Medium_Dataset_Apps
            |    |
            |    --- Large_Dataset_Apps
            |
            |
            --- GPU_APPS    (Kernels will be configured to use the CUDA SDK)
                 |
                 --- MINI_VVSMALL_Dataset_Apps
                 |
                 --- MINI_VSMALL_Dataset_Apps 
                 |
                 --- MINI_SMALL_Dataset_Apps    
                 |
                 --- MINI_Dataset_Apps
                 |   
                 --- Small_Dataset_Apps
                 |
                 --- Medium_Dataset_Apps
                 |
                 --- Large_Dataset_Apps
"""


targets_generation_root = "Generated_Dataset"

targets_generation_CPU_Kernels_Apps = os.path.join(targets_generation_root, "CPU_APPS")
targets_generation_GPU_Kernels_Apps = os.path.join(targets_generation_root, "GPU_APPS")

# Applications will be replicated with following variable data sizes against both the CPU and GPU
variable_data_specific_sub_dirs = ["MINI_VVSMALL", "MINI_VSMALL", "MINI_SMALL","MINI_DATASET", "SMALL_DATASET", "STANDARD_DATASET", "LARGE_DATASET", "EXTRALARGE_DATASET"]



CPU_common_makefile_template = """
#### INTEL SDK
# OPENCL_DEVICE_SELECTION = Either to CL_DEVICE_TYPE_CPU or to CL_DEVICE_TYPE_GPU

OpenCL_SDK=/usr/local/cuda

LIBPATH=-L${OpenCL_SDK}/lib64 -L${OpenCL_SDK}/shared/lib

INCLUDE=-I${OpenCL_SDK}/include/ -I${PATH_TO_UTILS}


LIB=-lOpenCL -lm

all:
	gcc -O3 -D<template> -DOPENCL_DEVICE_SELECTION=CL_DEVICE_TYPE_CPU ${INCLUDE} ${LIBPATH} ${CFILES} -o ${EXECUTABLE} ${LIB}

clean:
	rm -f *~ ${EXECUTABLE} *.txt
"""

GPU_common_makefile_template = """
#### CUDA SDK
# OPENCL_DEVICE_SELECTION = Either to CL_DEVICE_TYPE_CPU or to CL_DEVICE_TYPE_GPU

OpenCL_SDK=/usr/local/cuda

LIBPATH=-L${OpenCL_SDK}/lib64 -L${OpenCL_SDK}/shared/lib

INCLUDE=-I${OpenCL_SDK}/include/ -I${PATH_TO_UTILS}


LIB=-lOpenCL -lm

all:
	gcc -O3 -D<template> -DOPENCL_DEVICE_SELECTION=CL_DEVICE_TYPE_GPU ${INCLUDE} ${LIBPATH} ${CFILES} -o ${EXECUTABLE} ${LIB}

clean:
	rm -f *~ ${EXECUTABLE} *.txt
"""





# Will generate the required target directory structure
def generateRequiredDirectoryStrucutre():
    

    # This includes seperate DIRS for variable data sizes
    print(f"\n       --- Generating ROOT DIRS ---   \n")
    # Create the root dir
    if not os.path.exists(targets_generation_root):
        print(f"       -> Created: `{targets_generation_root}`")
        os.mkdir(targets_generation_root)

    # Generate the CPU and GPU root applications directories
    if not os.path.exists(targets_generation_CPU_Kernels_Apps):
        print(f"       -> Created: `{targets_generation_CPU_Kernels_Apps}`")
        os.mkdir(targets_generation_CPU_Kernels_Apps)
    
    if not os.path.exists(targets_generation_GPU_Kernels_Apps):
        print(f"       -> Created: `{targets_generation_GPU_Kernels_Apps}`")
        os.mkdir(targets_generation_GPU_Kernels_Apps)


    # Iterate over both CPU and GPU sub dirs and create the rest of the DIRS in them
    # This includes seperate DIRS for variable data sizes
    print(f"\n       --- Generating Sub DIRS for CPU and GPU kernel applications --- \n")
    for data_size_dir_to_generate in variable_data_specific_sub_dirs:

        # Generate dir for CPU
        variable_datasize_dir_CPU = os.path.join(targets_generation_CPU_Kernels_Apps, data_size_dir_to_generate)
        
        if not os.path.exists(variable_datasize_dir_CPU):
            print(f"        -> Created: `{variable_datasize_dir_CPU}`")
            os.mkdir(variable_datasize_dir_CPU)

        # Generate dir for GPU
        variable_datasize_dir_GPU = os.path.join(targets_generation_GPU_Kernels_Apps, data_size_dir_to_generate)
        
        if not os.path.exists(variable_datasize_dir_GPU):
            print(f"        -> Created: `{variable_datasize_dir_GPU}`")
            os.mkdir(variable_datasize_dir_GPU)



# The actual backend function for configureCommonUtilitiesForApps
def commonUtilitiesCreatorAndConfigureCORE(target_generation_path, is_for_cpu):
    
    #  Moving utilities dir for CPU apps (So we can configure these apps to utilize Intel SDK)
    for data_size_dir_to_generate in variable_data_specific_sub_dirs:

        # Copy the entire utilities folder to the destination dir(the specific variable data size application)
        destination = os.path.join(target_generation_path, data_size_dir_to_generate)

        print(f"        -> Configuring Utilities For: `{destination}`")

        # TODO; refactor needed; the following opeartions opens a new child process in an async manner; which can cause problems
        # As the very next lines are dependant on the result of this code
        _ = subprocess.Popen(["cp", "-r", "./POLYBENCH_KERNELS/utilities", destination], stdout = subprocess.PIPE)

        # At this stage we have common.mk file inside the copied utilities folder, which we need to remove
        # And update according to our cpu utilities template

        # removing the outdated common.mk
        time.sleep(0.01)
        outdated_makefile_to_remove = os.path.join(destination, "utilities" ,"common.mk")
        os.remove(outdated_makefile_to_remove)


        # The path for the updated MakeFile would be same as the outdated (Removed) MakeFile
        makefile_to_generate_path = outdated_makefile_to_remove
        # Generate updated custom tailored MakeFile for the specific device type data size

        
        if is_for_cpu:
            makefile_generated_from_template = CPU_common_makefile_template.replace("<template>", data_size_dir_to_generate)
        else:
            makefile_generated_from_template = GPU_common_makefile_template.replace("<template>", data_size_dir_to_generate)


        # Write the updated Makefile in the respestive application
        with open(makefile_to_generate_path, "w") as F:
            F.writelines(makefile_generated_from_template)  



# Is reponsible for copying the complete utilities dir into both CPU and GPU roots 
# So that the apps within, can utilize the utilities
# The reason of providing seperate utilities to CPU and GPU apps is, so that we can configure seperate SDK's for INTEL and NVIDIA
# Moreover, this also allows us to specify variable data size kernel applications
def configureCommonUtilitiesForApps():

    # Configure utilities for CPU kernel applications
    print(f"\n       --- Confiruing CPU based applications utilities and MakeFile ---   \n")
    commonUtilitiesCreatorAndConfigureCORE(targets_generation_CPU_Kernels_Apps, is_for_cpu=True)

    # Configure utilities for GPU kernel applciations
    print(f"\n       --- Confiruing GPU based applications utilities and MakeFile ---   \n")
    commonUtilitiesCreatorAndConfigureCORE(targets_generation_GPU_Kernels_Apps, is_for_cpu=False)


def copyKernelApplications():
    
    # Get the list of available kernel applications in POLYBENCH_APPS_ROOT_PATH
    # I am doing this so that I can copy applications on individual level
    # Copying them in respective dirs one by one
    # I could have have used the wild card `*` but for some reason it does not work
    # When I issue commands using subprocess.Popen()
    available_kernel_names = os.listdir(POLYBENCH_APPS_ROOT_PATH)

    for data_size_dir_to_generate in variable_data_specific_sub_dirs:

        # Copy the entire utilities folder to the destination dir(the specific variable data size application)
        destination = os.path.join(targets_generation_CPU_Kernels_Apps, data_size_dir_to_generate)


        print(f"\n       --- Copying Kernel Applications For CPU -> {data_size_dir_to_generate}---   ")
        for K in available_kernel_names:
            _ = subprocess.Popen(["cp", "-r", os.path.join(POLYBENCH_APPS_ROOT_PATH, K), destination], stdout = subprocess.PIPE)

        


         # Copy the entire utilities folder to the destination dir(the specific variable data size application)
        destination = os.path.join(targets_generation_GPU_Kernels_Apps, data_size_dir_to_generate)
        
        print(f"       --- Copying Kernel Applications For GPU -> {data_size_dir_to_generate}---   \n")
        for K in available_kernel_names:
         _ = subprocess.Popen(["cp", "-r", os.path.join(POLYBENCH_APPS_ROOT_PATH_GPU, K), destination], stdout = subprocess.PIPE)

    

def main():

    print("\n\n     Polybench Variable Dataset Generation Utility\n")

    # Generate the required directory structure
    generateRequiredDirectoryStrucutre()

    # Copy common utilities in the roots of CPU and GPU and all of their sub apps
    configureCommonUtilitiesForApps()


    # Copy the kernel applications for both the CPU and the GPU
    copyKernelApplications()



if __name__ == "__main__":
    main()
