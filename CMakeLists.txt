cmake_minimum_required(VERSION 3.0.0)
project(qlazy)
add_library(qlz SHARED qlazy/lib/c/qsystem.c qlazy/lib/c/init.c qlazy/lib/c/qgate.c
  qlazy/lib/c/qc.c qlazy/lib/c/qstate.c qlazy/lib/c/mdata.c qlazy/lib/c/gbank.c qlazy/lib/c/spro.c
  qlazy/lib/c/observable.c qlazy/lib/c/densop.c qlazy/lib/c/stabilizer.c qlazy/lib/c/misc.c
  qlazy/lib/c/message.c qlazy/lib/c/help.c)
add_executable(qlazy qlazy/lib/c/qlazy.c)
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
