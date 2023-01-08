PROG = qlazy
PROG_OBJ = qlazy.o qsystem.o
PROG_SRC = qlazy.c qsystem.c

INC = qlazy.h

LIB = libqlz.so
LIB_OBJ_BASE = qg.o qc.o qstate.o mdata.o gbank.o spro.o \
        observable_base.o densop.o stabilizer.o misc.o message.o help.o \
	cmem.o qgate.o qcirc.o random.o tagtable.o
LIB_SRC_BASE = qg.c qc.c qstate.c mdata.c gbank.c spro.c \
        observable_base.c densop.c stabilizer.c misc.c message.c help.c \
	cmem.c qgate.c qcirc.c random.c tagtable.c
LIB_OBJ_GPU = qstate_gpu.o gpu.o
LIB_SRC_GPU = qstate_gpu.cu gpu.cu

# install directory (edit here to your environment)
INSTALL_BIN_DIR = ~/bin
INSTALL_LIB_DIR = ~/lib
INSTALL_INC_DIR = ~/include

# defalut: GPU is not available
GPU = no

# get current version number
CURRENT_VERSION=$$(cat VERSION)

#===============================================================================
# GPU available or not

ifeq ($(GPU),no)  # GPU not available

LIB_OBJ = $(LIB_OBJ_BASE)
LIB_SRC = $(LIB_SRC_BASE)

CC = gcc
CC_LINK = gcc

# CFLAG_CC = -fPIC -fopenmp -Wall -O2 -DDEV -DUSE_LIBREADLINE # link libreadline.so
CFLAG_CC = -fPIC -fopenmp -Wall -O2 -DDEV
CFLAG_LINK = $(CFLAG_CC)

IFLAG = -I.
LFLAG = -L.

# PROG_OPTION = -lqlz -lreadline # link libreadline.so
PROG_OPTION = -lqlz
LIB_OPTION = -lm
# LIB_OPTION =  -Wl,-Bstatic,-lm,-Bdynamic

else  # GPU available

# CUDA include directory (edit here to your CUDA environment)
CUDA_INC_DIR = /usr/local/cuda/include

LIB_OBJ = $(LIB_OBJ_BASE) $(LIB_OBJ_GPU)
LIB_SRC = $(LIB_SRC_BASE) $(LIB_SRC_GPU)

CC = g++
CC_LINK = nvcc

CFLAG_CC = -fPIC -fopenmp -Wall -O2 -DDEV -DUSE_GPU
CFLAG_LINK = --default-stream per-thread -Xcompiler '-fPIC -fopenmp -Wall -O2 -DUSE_GPU --std=c++03' -ccbin g++

IFLAG = -I. -I$(CUDA_INC_DIR)
LFLAG = -L.

# PROG_OPTION = -lqlz -lreadline # link libreadline.so
PROG_OPTION = -lqlz
LIB_OPTION = -lm -lcurand

.SUFFIXES: .cu
.cu.o:
	$(CC_LINK) --std=c++03 $(CFLAG_LINK) $(IFLAG) -c $<

endif

#===============================================================================

$(PROG): $(PROG_OBJ) $(LIB)
	$(CC_LINK) -o $@ $(CFLAG_LINK) $(LFLAG) $(IFLAG) $(PROG_OBJ) $(PROG_OPTION)

$(LIB): $(LIB_OBJ)
	$(CC_LINK) $(CFLAG_LINK) $(IFLAG) -shared $(LIB_OBJ) -o $@ $(LIB_OPTION)

$(PROG_OBJ): $(INC) $(PROG_SRC)

$(LIB_OBJ): $(INC) $(LIB_SRC)

cpu:
	make GPU=no

gpu:
	make GPU=yes

tags:
	etags *.[ch]

clean:
	rm -f $(PROG_OBJ) $(LIB_OBJ_BASE) $(LIB_OBJ_GPU) $(LIB) $(PROG) TAGS; \
	find ../../ | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

install:
	cp $(PROG) $(INSTALL_BIN_DIR); \
	cp $(LIB) $(INSTALL_LIB_DIR); \
	cp $(INC) $(INSTALL_INC_DIR); \

.SUFFIXES: .o .c
.c.o:
	$(CC) $(CFLAG_CC) $(IFLAG) -c $<
