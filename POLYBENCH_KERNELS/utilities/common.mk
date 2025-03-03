#### INTEL SDK

# OpenCL_SDK=/opt/intel/system_studio_2020/opencl/SDK

# INCLUDE=-I${OpenCL_SDK}/include/CL -I${PATH_TO_UTILS}

# LIBPATH=-L${OpenCL_SDK}/lib64 -L${OpenCL_SDK}/shared/lib
#### CUDA SDK

OpenCL_SDK=/usr/local/cuda


INCLUDE=-I${OpenCL_SDK}/include/ -I${PATH_TO_UTILS}

# LIBPATH=-L${OpenCL_SDK}/lib 
LIBPATH=-L${OpenCL_SDK}/lib64 -L${OpenCL_SDK}/shared/lib


LIB=-lOpenCL -lm

all:
	gcc -O3 ${INCLUDE} ${LIBPATH} ${CFILES} -o ${EXECUTABLE} ${LIB}

clean:
	rm -f *~ ${EXECUTABLE} *.txt
