#include <stdio.h>
#include <iostream>

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

// Device code
// tell compiler that following func is device code, not host
__global__
void cuda_kernel() { // return type is always void
    int row_offset = blockDim.x * blockDim.x * threadIdx.x;
    int col_offset = gridDim.x * blockIdx.y * blockDim.x * blockDim.y + blockDim.x * threadIdx.y;

    int tid = threadIdx.x;
    int bid = blockIdx.x;
    int gid = tid + col_offset + row_offset;

    printf("threadId: %d, blockId: %d, globalId: %d\n", tid, bid, gid);
}

void device_prop() {
    int deviceNo = 0;
    cudaDeviceProp iGpuProp;
    
    cudaGetDeviceProperties(&iGpuProp, deviceNo);

    std::cout << "Max block size: ";
    for (size_t i = 0; i < 3; i++) {
        std::cout << iGpuProp.maxThreadsDim[i] << " ";
    }
    std::cout << std::endl;

    std::cout << "Max grid size: ";
    for (size_t i = 0; i < 3; i++) {
        std::cout << iGpuProp.maxGridSize[i] << " ";
    }
    std::cout << std::endl;

    std::cout << "Max thread per block: " << iGpuProp.maxThreadsPerBlock << std::endl;
}

// Host code
int main() {
    std::cout << "First CUDA programme" << std::endl;

    device_prop();

    // total threads in X, Y, Z dimension
    int nx, ny, nz;

    nx = 128;
    ny = nz = 1;

    // in 1 block: 32 threads in x, 1 thread in y & z
    dim3 block(32, 1, 1);

    // in 1 grid: 4 block in x, 1 block in y & z
    dim3 grid(nx/block.x, ny/block.y, nz/block.z);

    cuda_kernel <<< grid, block >>> (); 

    // host wait for device to execute
    cudaDeviceSynchronize();
    
    // destroy CUDA context, device alloc ...
    cudaDeviceReset();

    return 0;
}