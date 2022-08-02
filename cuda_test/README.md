# 0. Refer documents
https://medium.com/analytics-vidhya/cuda-memory-model-823f02cef0bf

# 1. Hello world
nvcc -ccbin g++ 1_hello_world.cu -I/usr/local/cuda/include

# 2. Array Accumulating (test on Jetson Xavier NX)
nvcc -ccbin g++ 2_1_array_accumelating_pageable_mem.cu -I/usr/local/cuda/include
nvcc -ccbin g++ 2_2_array_accumelating_pin_mem.cu -I/usr/local/cuda/include
nvcc -ccbin g++ 2_3_array_accumelating_map_mem.cu -I/usr/local/cuda/include
nvcc -ccbin g++ 2_4_array_accumelating_unified_mem.cu -I/usr/local/cuda/include

- Mem size (bytes): 1920x1080x3

- Processing time GPU = Memory transfer GPU (Host to device) + Compute time GPU

- Pageable mem:
Processing time CPU: 8.18026 ms  
Processing time GPU: 13.4784 ms  
Memory transfer GPU: 7.46821 ms  
Compute time GPU: 6.01019 ms   

- Pin mem:
Processing time CPU: 8.77639 ms   
Processing time GPU: 5.14921 ms  
Memory transfer GPU: 2.40147 ms  
Compute time GPU: 2.74775 ms  

- Map mem:
Processing time CPU: 9.83721 ms  
Processing time GPU: 1.72764 ms  
Memory transfer GPU: 0.000288 ms  
Compute time GPU: 1.72735 ms  

- Unified mem:
Processing time CPU: 8.76121 ms  
Processing time GPU: 1.69877 ms  
Memory transfer GPU: 0.000224 ms  
Compute time GPU: 1.69855 ms  