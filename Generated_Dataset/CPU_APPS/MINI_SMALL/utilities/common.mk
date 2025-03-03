
#### INTEL SDK
# OPENCL_DEVICE_SELECTION = Either to CL_DEVICE_TYPE_CPU or to CL_DEVICE_TYPE_GPU

OpenCL_SDK=/usr/local/cuda

LIBPATH=-L${OpenCL_SDK}/lib64 -L${OpenCL_SDK}/shared/lib

INCLUDE=-I${OpenCL_SDK}/include/ -I${PATH_TO_UTILS}


LIB=-lOpenCL -lm

all:
	gcc -O3 -DMINI_SMALL -DOPENCL_DEVICE_SELECTION=CL_DEVICE_TYPE_CPU ${INCLUDE} ${LIBPATH} ${CFILES} -o ${EXECUTABLE} ${LIB}

clean:
	rm -f *~ ${EXECUTABLE} *.txt
