cmake_minimum_required(VERSION 3.0.0)
project(qlazy)
add_library(qlz SHARED qsystem.c init.c qg.c
  qc.c qstate.c mdata.c gbank.c spro.c
  observable.c densop.c stabilizer.c misc.c message.c help.c cmem.c qcirc.c)
add_executable(qlazy qlazy.c)
target_link_libraries(qlz m readline)
target_link_libraries(qlazy qlz)

set(CMAKE_C_FLAGS "-fPIC -Wall -O2")
set(CMAKE_CXX_FLAGS "-fPIC -Wall -O2")

# for OpenMP
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
  set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
endif()
