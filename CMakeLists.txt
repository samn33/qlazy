cmake_minimum_required(VERSION 3.10.0)
project(qlazy)

set(DEFAULT_USE_GPU No)

if(NOT DEFINED USE_GPU)
  set(USE_GPU ${DEFAULT_USE_GPU})
endif()

set(LIB_SRC_BASE qlazy/lib/c/qg.c qlazy/lib/c/qc.c
  qlazy/lib/c/qstate.c qlazy/lib/c/mdata.c qlazy/lib/c/gbank.c qlazy/lib/c/spro.c
  qlazy/lib/c/observable_base.c qlazy/lib/c/densop.c qlazy/lib/c/stabilizer.c
  qlazy/lib/c/misc.c qlazy/lib/c/message.c qlazy/lib/c/help.c
  qlazy/lib/c/cmem.c qlazy/lib/c/qgate.c qlazy/lib/c/qcirc.c qlazy/lib/c/random.c
  qlazy/lib/c/tagtable.c)

set(LIB_SRC_GPU qlazy/lib/c/gpu.cu qlazy/lib/c/qstate_gpu.cu)

if(USE_GPU)

  enable_language(CUDA)

  find_package(CUDA REQUIRED)
  message("!!! USE_GPU !!!")
  message("Cuda version: " ${CUDA_VERSION})
  message("Cuda Compiler ID: " ${CMAKE_CUDA_COMPILER_ID})
  message("Cuda Compiler version: " ${CMAKE_CUDA_COMPILER_VERSION})

  set(CMAKE_C_COMPILER g++)
  set(CMAKE_CXX_COMPILER g++)

  add_definitions(-O2 -DUSE_GPU -I/usr/local/cuda/include/ -std=c++03)
  
  add_executable(qlazy qlazy/lib/c/qlazy.c qlazy/lib/c/qsystem.c)
  add_library(qlz SHARED ${LIB_SRC_BASE} ${LIB_SRC_GPU})

  set_target_properties(qlz PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
  set_property(TARGET qlz PROPERTY CUDA_SEPARABLE_COMPILATION ON)

  include_directories(qlazy/lib/c/ /usr/local/include/cuda/)

  # target_link_libraries(qlz m readline gomp ${CUDA_curand_LIBRARY}) # link libreadline.so
  target_link_libraries(qlz m gomp ${CUDA_curand_LIBRARY})
  target_link_libraries(qlazy qlz)

  list(APPEND CMAKE_CUDA_FLAGS "--default-stream per-thread")
  message("CMAKE_CUDA_FLAGS: " ${CMAKE_CUDA_FLAGS})

  set(CMAKE_C_FLAGS ${CMAKE_C_FLAGS} "-mtune=native -march=native -mfpmath=both")
  set(CMAKE_CXX_FLAGS ${CMAKE_C_FLAGS})
  
  set(CUDA_HOST_COMPILER g++)
  
  # for OpenMP
  find_package(OpenMP REQUIRED)
  if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -Xcompiler=${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_CXX_FLAGS}")
  endif()

else()

  message("!!! Not USE_GPU !!!")
  add_library(qlz SHARED ${LIB_SRC_BASE})
  add_executable(qlazy qlazy/lib/c/qlazy.c qlazy/lib/c/qsystem.c)
  target_link_libraries(qlz m)
  # target_link_libraries(qlazy readline tinfo qlz) # link libreadline.so
  target_link_libraries(qlazy qlz)

  set(CMAKE_C_FLAGS "-fPIC -Wall -O2")
  set(CMAKE_CXX_FLAGS "-fPIC -Wall -O2")

  # for OpenMP
  find_package(OpenMP REQUIRED)
  if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
  endif()

endif()
