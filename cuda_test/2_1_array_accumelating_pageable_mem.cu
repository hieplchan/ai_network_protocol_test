#include <stdio.h>
#include <iostream>
#include <chrono>

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#define NUM_EXECUTE 100

// Device code
__global__ void array_sum(int *d_a, int *d_b, int *d_c, int size) {
    int gid = blockDim.x * blockIdx.x + threadIdx.x;
    if (gid < size) {
        d_c[gid] = d_a[gid] + d_b[gid];
    }
}

// Host code
int main() {
    std::cout << "Array accumalating CUDA programme" << std::endl;

    int size = 1920*1080*3;
    int block_size = 128;
    int NUM_BYTES = sizeof(int) * size;

    std::chrono::high_resolution_clock::time_point start_point;
    std::chrono::high_resolution_clock::time_point end_point;
    std::chrono::high_resolution_clock::time_point memcpy_point;
    std::chrono::duration<double, std::milli> delta;
    std::chrono::duration<double, std::milli> delta_memcpy;


    // Host memmory alloc
    int *h_a, *h_b, *h_c;
    h_a = (int *)malloc(NUM_BYTES);
    h_b = (int *)malloc(NUM_BYTES);
    h_c = (int *)malloc(NUM_BYTES);

    // Prepare device memory
    int *d_a, *d_b, *d_c;
    cudaMalloc((int **)&d_a, NUM_BYTES);
    cudaMalloc((int **)&d_b, NUM_BYTES);
    cudaMalloc((int **)&d_c, NUM_BYTES);

    // Prepare host data
    for (size_t i = 0; i < size; i++) {
        h_a[i] = 10;
        h_b[i] = 20;
    }
    memset(h_c, 0, NUM_BYTES);

    /* CPU version */
    for (size_t k = 0; k < NUM_EXECUTE; k++) {
        start_point = std::chrono::high_resolution_clock::now();
        for (size_t i = 0; i < size; i++) {
            h_c[i] = h_a[i] + h_b[i];
        }
        end_point = std::chrono::high_resolution_clock::now();  
        delta = (end_point - start_point);  
        // std::cout << "h_c[10]: " << h_c[10] << std::endl;
        std::cout << "Processing time CPU: " << delta.count() << " ms" << std::endl;
    }

    /* GPU version */
    memset(h_c, 0, NUM_BYTES);
    dim3 block(block_size);
    dim3 grid(size/block_size);

    // Transfer data from host to device using pageable memory
    for (size_t k = 0; k < NUM_EXECUTE; k++) {
        start_point = std::chrono::high_resolution_clock::now();

        cudaMemcpy(d_a, h_a, NUM_BYTES, cudaMemcpyHostToDevice);
        cudaMemcpy(d_b, h_b, NUM_BYTES, cudaMemcpyHostToDevice);

        memcpy_point = std::chrono::high_resolution_clock::now();  

        // Kernel launch
        array_sum <<< grid, block >>> (d_a, d_b, d_c, NUM_BYTES);
        cudaDeviceSynchronize();    
        cudaMemcpy(h_c, d_c, NUM_BYTES, cudaMemcpyDeviceToHost);

        end_point = std::chrono::high_resolution_clock::now();  
        delta = (end_point - start_point);  
        // std::cout << "h_c[10]: " << h_c[10] << std::endl;
        std::cout << "Processing time GPU: " << delta.count() << " ms" << std::endl;
        delta = (end_point - memcpy_point);  
        delta_memcpy = (memcpy_point - start_point);
        std::cout << "Memory transfer GPU: " << delta_memcpy.count() << " ms" << std::endl;
        std::cout << "Compute time GPU: " << delta.count() << " ms" << std::endl;
    }

    // Free device memory
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);

    // Free host memory
    free(h_a);
    free(h_b);
    free(h_c);

    return 0;
}