
rm -rf OUTPUT_FILES
mkdir OUTPUT_FILES

NPROC=`grep ^NPROC DATA/Par_file | grep -v -E '^[[:space:]]*#' | cut -d = -f 2 | cut -d \# -f 1`
echo "The simulation will run on NPROC = " $NPROC " MPI tasks"

mpirun -np $NPROC ./bin/xmeshfem2D

mpirun -np $NPROC ./bin/xspecfem2D


