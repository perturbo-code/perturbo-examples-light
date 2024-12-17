FC = gfortran

FCFLAGS = -I$(H5_ROOT)/include

LDFLAGS = -L/usr/lib64

HDF5_DIR = /path/hdf5/gcc/1.12.0/lib

HDF5_LIB = $(HDF5_DIR)/libhdf5_fortran.a $(HDF5_DIR)/libhdf5_hl_fortran.a \
		   $(HDF5_DIR)/libhdf5_hl.a $(HDF5_DIR)/libhdf5.a

H5_ROOT = /path/lib64/fortran/h5

H5_LIB   = $(H5_ROOT)/lib64/libh5fortran.a

LIB = -lpthread -ldl -lm -lz

LIBS = $(H5_LIB) $(HDF5_LIB) $(LIB)

all: qtensor

qtensor: qtensor.o
	@$(FC) -o $@ $< $(LDFLAGS)  $(LIBS)
	@echo "gfortran -o qtensor qtensor.o"

qtensor.o: qtensor.f90
	@$(FC) $(FCFLAGS) -c $<
	@echo "gfortran -c qtensor.f90"

clean:
	rm -f qtensor qtensor.o
