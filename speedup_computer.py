import os 
import subprocess
import time
import csv
import re


# will be used for probing number of available kernel applications
all_kernel_apps_cpu_mini_dataset_path = "Generated_Dataset/CPU_APPS/MINI_DATASET"

dataset_filename = "speedup_data.csv"


# Will Compile all the combinations of kernels
def compileAllCombinationsOfKernels():


    # Probe the avaiable kernel applicatons
    # For this purpose we can probe any folder containing all the kernel applicaions
    # PS: We have numerous folders containing same kernel applications; 
    # but with different conf; e.g, data size and CPU and GPU execcution flag
    if os.path.exists(all_kernel_apps_cpu_mini_dataset_path):
        
        kernel_apps = os.listdir(all_kernel_apps_cpu_mini_dataset_path)

        kernel_apps.remove("utilities")

        path_base = "Generated_Dataset"
        cpu_folder_name = "CPU_APPS"
        gpu_folder_name = "GPU_APPS"

        datasize_variants = ["MINI_VVSMALL", "MINI_VSMALL", "MINI_SMALL", "MINI_DATASET", "SMALL_DATASET", "STANDARD_DATASET", "LARGE_DATASET", "EXTRALARGE_DATASET"]

        # Iterate over all the datasize_variants
            # Iterate over all the applications
                # Compile them
                    # Make a running time comparison between CPU and GPU application
                        # Push results to csv

                
        complied_anything  = False

        for datasize_variant in datasize_variants:

            for kernel_app in kernel_apps:

                #CPU kernel compilation
                # Get the path for kernel_app ; inside CPU_APPS for datasize_variant    
                cpu_app = os.path.join(path_base, cpu_folder_name, datasize_variant, kernel_app) 

                # if the binary exists then skip the compilation
                if not os.path.exists(os.path.join(cpu_app, kernel_app)):
                    # Compile
                    compilation_ouput = subprocess.Popen(["make", "--directory", cpu_app])
                    time.sleep(0.01)
                    complied_anything = True

                #GPU kernel compilation
                # Get the path for kernel_app ; inside CPU_APPS for datasize_variant
                gpu_app = os.path.join(path_base, gpu_folder_name, datasize_variant, kernel_app) 

                # if the binary exists then skip the compilation
                if not os.path.exists(os.path.join(gpu_app, kernel_app)):
                    # Compile
                    compilation_ouput = subprocess.Popen(["make", "--directory", gpu_app])
                    time.sleep(0.01)
                    complied_anything = True

                

        if not complied_anything:
            print("Compilations Skipped; Kernels already compiled.....")

        return True

    else:
        print("Unable to identify available kernel applications; quitting..........")
        return False


def computeRunningTimesOfKernelsOnCPUAndGPU():  

    kernel_apps = os.listdir(all_kernel_apps_cpu_mini_dataset_path)

    kernel_apps.remove("utilities")

    path_base = "Generated_Dataset"
    cpu_folder_name = "CPU_APPS"
    gpu_folder_name = "GPU_APPS"

    datasize_variants = ["MINI_VVSMALL", "MINI_VSMALL", "MINI_SMALL", "MINI_DATASET", "SMALL_DATASET", "STANDARD_DATASET", "LARGE_DATASET", "EXTRALARGE_DATASET"]



    # Reading the already computed runtimes from the csv so we may skip those
    already_computed_runtimes = [] # Structure -> "Datasize + kernel"

    with open(dataset_filename, "r") as csv_reader_handle:

        reader = csv.reader(csv_reader_handle, delimiter=",")

        for row in reader:

            unique_kernel_app_signature = row[0] +"+"+ row[1]

            already_computed_runtimes.append(unique_kernel_app_signature)




    for datasize_variant in datasize_variants:

        for kernel_app in kernel_apps:
            
            unique_kernel_signature = datasize_variant + "+" + kernel_app

            if unique_kernel_signature in already_computed_runtimes:
                print(f"skipped Runtime Computation For {unique_kernel_signature}")
                continue

            #CPU kernel runtime computation
            cpu_app = os.path.join(path_base, cpu_folder_name, datasize_variant, kernel_app) 


            current_dir = os.getcwd()

            os.chdir(cpu_app)
            kernel_output = subprocess.run(["./" + kernel_app], capture_output=True,text=True)

            kernel_output = kernel_output.stdout

            # The complete kernel output contains a lot more information then what we need
            # We will narrow our required output using a some predefined string as follows
            # Note even though the output says that we are outputting GPU time
            # But its not true, we are actually running kernels on the CPU
            # As the kernels located inside the cpu folder have been configured to run on the CPU
            str_to_narrow_with = "GPU Time in seconds:"
            narrowed_runtime_in_seconds = kernel_output[kernel_output.find(str_to_narrow_with) + len(str_to_narrow_with):]

            time_took_in_seconds_CPU = None
            try:
                 # Extract float from str
                 time_took_in_seconds_CPU = float(narrowed_runtime_in_seconds)

            except ValueError:
                print(f"EXECEPTION OCCURRED :: Current Device -> CPU, Datasize -> {datasize_variant} and Kernel -> {kernel_app}")
                print("Value in Question :::", narrowed_runtime_in_seconds)

            # Change back to the original dir, so that we can cd into other relative dirs
            os.chdir(current_dir)

            ###### Compute RUNTIME of same kernel but this time on the GPU


            #CPU kernel runtime computation
            gpu_app = os.path.join(path_base, gpu_folder_name, datasize_variant, kernel_app) 


            current_dir = os.getcwd()

            os.chdir(gpu_app)
            kernel_output = subprocess.run(["./" + kernel_app], capture_output=True,text=True)

            kernel_output = kernel_output.stdout

            # The complete kernel output contains a lot more information then what we need
            # We will narrow our required output using a some predefined string as follows
            str_to_narrow_with = "GPU Time in seconds:"
            narrowed_runtime_in_seconds = kernel_output[kernel_output.find(str_to_narrow_with) + len(str_to_narrow_with):]

            time_took_in_seconds_GPU = None
            try:
                 # Extract float from str
                potenrial_float = re.search("(\d+.\d+)", narrowed_runtime_in_seconds).group(1)
                time_took_in_seconds_GPU = float(potenrial_float)
            except ValueError as E:
                print(f"Error Reading GPU Memory @ Kernel -> {kernel_app} @ Datasize -> {datasize_variant}")
                print(E)

            # Change back to the original dir, so that we can cd into other relative dirs
            os.chdir(current_dir)






            # Write results to the CSV in following format
            # DataVariant,KernelName,CPU_TIME_IN_SECONDS,GPU_TIME_IN_SECONDS,LABEL
            # e.g
            # MINI_DATASET,2mm,0.0345,0.0444,CPU_SUITABLE
            with open(dataset_filename, "a") as dataset_csv_file:
                
                writer = csv.writer(dataset_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                print("GPU-type -> ",type(time_took_in_seconds_CPU))
                print("GPU-type -> ",type(time_took_in_seconds_GPU))
                label = "CPU_SUITABLE" if time_took_in_seconds_CPU < time_took_in_seconds_GPU else "GPU_SUITABLE"
                writer.writerow([datasize_variant, kernel_app, time_took_in_seconds_CPU, time_took_in_seconds_GPU, label])

            # break
        
        # break


def main():
    
    successful =compileAllCombinationsOfKernels()

    # Skip speedup computations; if there were any problems during the kernel compilation phase
    if successful:
        computeRunningTimesOfKernelsOnCPUAndGPU()
    


if __name__ == "__main__":

    main()
