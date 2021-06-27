PROG = qlazy
PROG_OBJ = qlazy.o
PROG_SRC = qlazy.c

INC = qlazy.h

LIB = libqlz.so
LIB_OBJ_BASE = qsystem.o init.o qg.o qc.o qstate.o mdata.o gbank.o spro.o \
        observable.o densop.o stabilizer.o misc.o message.o help.o cmem.o qcirc.o
LIB_SRC_BASE = qsystem.c init.c qg.c qc.c qstate.c mdata.c gbank.c spro.c \
        observable.c densop.c stabilizer.c misc.c message.c help.c cmem.c qcirc.c

# install directory (edit here to your environment)
INSTALL_BIN_DIR = ~/bin
INSTALL_LIB_DIR = ~/lib
INSTALL_INC_DIR = ~/include

LIB_OBJ = $(LIB_OBJ_BASE)
LIB_SRC = $(LIB_SRC_BASE)

CC = gcc
CC_LINK = gcc

CFLAG_CC = -fPIC -fopenmp -Wall -O2 -DDEV
# CFLAG_CC = -fPIC -Wall -O2 -DDEV
CFLAG_LINK = $(CFLAG_CC)

IFLAG = -I.
LFLAG = -L.
LIB_OPTION =  -lm -lreadline

$(PROG): $(PROG_OBJ) $(LIB)
	$(CC_LINK) -o $@ $(CFLAG_LINK) $(LFLAG) $(IFLAG) $(PROG_OBJ) $(LIB_OPTION) -lqlz

$(LIB): $(LIB_OBJ)
	$(CC_LINK) $(CFLAG_LINK) $(IFLAG) -shared $(LIB_OBJ) -o $@ $(LIB_OPTION)

$(PROG_OBJ): $(INC) $(PROG_SRC)

$(LIB_OBJ): $(INC) $(LIB_SRC)

tags:
	etags *.[ch]

clean:
	rm -f $(PROG_OBJ) $(LIB_OBJ) $(LIB) $(PROG) TAGS; \
	find ../../ | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

install:
	cp $(PROG) $(INSTALL_BIN_DIR); \
	cp $(LIB) $(INSTALL_LIB_DIR); \
	cp $(INC) $(INSTALL_INC_DIR); \

.SUFFIXES: .o .c
.c.o:
	$(CC) $(CFLAG_CC) $(IFLAG) -c $<
