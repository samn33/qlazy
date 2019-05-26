cmake_minimum_required(VERSION 3.0.0)
project(qlazy)
add_library(Qlazy SHARED qsystem.c init.c cimage.c qgate.c
		  qcirc.c qstate.c mdata.c gbank.c spro.c
		  observable.c misc.c message.c help.c)
add_executable(qlazy qlazy.c)
target_link_libraries(Qlazy m readline)
target_link_libraries(qlazy Qlazy)
