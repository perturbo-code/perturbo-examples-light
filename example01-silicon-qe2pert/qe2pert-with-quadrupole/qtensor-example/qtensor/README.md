   This is a small script to convert the Quadrupole tensor which is generate via Abinit 9.8.2 
from a txt-format to the hdf5-format with Fortran. There are some preparatory work before use 
it in your own system.

## HDF5 Library

    To be consistent with the programs used on the cluster, we recommend using the HDF5 library 
version 1.12.0. You can download it via follow command:

```bash
   wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz
```

    Once you have it, you can execute the following command to compile it (Note that here we compile it via gcc 13.1.0):

```bash
   tar -xf hdf5-1.12.0.tar.gz && cd hdf5-1.12.0
   mkdir build && cd build
   ../configure --prefix=/path/to/your/hdf5/gcc/1.12.0 --enable-fortran
   make -j32 && make test && make install
```

    Note that if the compilation process encounters the following error, you can try to execute this command:

```bash
   error: maximum decimal precision for C... configure: error: C program fails to build or run!
   
   unset LIBRARY_PATH CPATH C_INCLUDE_PATH PKG_CONFIG_PATH CPLUS_INCLUDE_PATH INCLUDE
```

    If you're fortunate, you'll have an hdf5 library. Please check the `/path/to/your/hdf5/gcc/1.12.0/include` 
path for hdf5.mod headers and the `/path/to/your/hdf5/gcc/1.12.0/lib` directory for *fortran* libraries.
    
    Then you can redact a hdf5.env file for follow-up using via `source ~/hdf5.env`

```bash
   vim ~/hdf5.env
   
   module unload mathlib/hdf5/intel/1.12.0
   
   HDF5_HOME=$HOME/software/hdf5/gcc/1.12.0
   
   export PATH=$HDF5_HOME/bin:$PATH
   export LIBRARY_PATH=$HDF5_HOME/lib:$LIBRARY_PATH
   export LD_LIBRARY_PATH=$HDF5_HOME/lib:$LD_LIBRARY_PATH
   export INCLUDE=$HDF5_HOME/include:$INCLUDE
   
```
    
## H5fortran Library

    In this script, we use the h5fortran library to create HDF5 files more conveniently. First of all, we need 
to download the h5fortran library.
    
```bash
   git clone https://github.com/geospace-code/h5fortran.git && cd h5fortran
   module load compiler/cmake/3.20.1
   cmake -B build -DCMAKE_PREFIX_PATH=$HOME/software/hdf5/gcc/1.12.0 -DCMAKE_INSTALL_PREFIX=$HOME/software/lib/fortran/h5
   cmake --build build
   cmake --install build
```

    where the `-DCMAKE_PREFIX_PATH` command specifies the path of the hdf5 library, and `-DCMAKE_INSTALL_PREFIX` specifies 
the installation path.
    
    Now you can check that whether the `$HOME/software/lib/fortran/h5/include` path include `h5fortran.mod` file and 
`$HOME/software/lib/fortran/h5/lib64` path include `libh5fortran.a` library.
    
## Compile this script

    After all preparatory work, now we can compile this script with `make`, you nee modify the `Makefile` file:

```bash

FC=gfortran

HDF5_DIR = /path/to/your/hdf5/lib  # lib level
H5_ROOT = /path/to/your/h5fortran  # top dir level

HDF5_LIB = $(HDF5_DIR)/libhdf5_fortran.a \
           $(HDF5_DIR)/libhdf5_hl_fortran.a \
		   $(HDF5_DIR)/libhdf5_hl.a \
		   $(HDF5_DIR)/libhdf5.a

H5_LIB   = $(H5_ROOT)/lib64/libh5fortran.a

FFLAGS=-I$(H5_ROOT)/include

LDFLAGS = -L/usr/lib64

LIB = -lpthread -ldl -lm -lz

LIBS = $(H5_LIB) $(HDF5_LIB) $(LIB)

all: qtensor

qtensor: qtensor.o
	$(FC) -o $@ $< $(LDFLAGS)  $(LIBS)

qtensor.o: qtensor.f90
	$(FC) $(FFLAGS) -c $<

clean:
	rm -f qtensor qtensor.o

```

   Then you can type `make` to obtain the executable file `qtensor`, before executing it please do not forget type 
`source ~/hdf5.env` command. 

## Obtain qtensor

    Before executing the `qtensor` you need have a `anaddb` output file which always have a name `tlw_3.abo`. 
If it already existed, you can simplely type `./qtensor` command to obtain a `qtensor.h5` file, you can rename it to 
`prefix_qtensor.h5` for `qe2pert.x`. Due to that the `prefix` of your system does not include in `tlw_3.abo`, we can 
not automatically identify it, therefore you have to do it by hand.
    
## Use precompiled scripts

    You can also simplely use this script by adding the path `/data/shared/jygong/software/bin` to your own `~/.bashrc` 
file and load the gcc 11.2.0 before executing it via `module load compiler/gcc/11.2.0`. For instance:
    
```bash
vim ~/.bashrc

# load gcc 11.2.0 otherwise you will get an error about can not found library after executing the script
module load compiler/gcc/11.2.0

export PATH=/data/shared/jygong/software/bin:$PATH
```

    Then you can quit the vim via `:wq` command, and refersh the environment variable via `source ~/.bashrc` command. Now 
you can type the `qtensor` command in your command-line and you will obtain a `qtensor.h5` after that.
    
    NOTE!!! We use the tlw_3.abo as the anaddb output file, please do not modify it, in oher words, do not change the input 
file name tlw_3.abi for anaddb.
