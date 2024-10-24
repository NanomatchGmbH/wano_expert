#!/bin/bash

export OMP_NUM_THREADS=1

# Here we check, whether variables are set and add them to the mpirun exports. This is not required for mpirun with PBS/Torque, but required with everything else.
# We could also specify only the required ones, but we do not know that a priori (i.e. whether Turbomole or Gaussian is to be used.
# To avoid warnings, we therefore check first whether something is set and only then add it to the command.
function varisset {
        if [ -z ${!1+x} ]
        then
                echo "false"
        else
                echo "true"
        fi
}
environmentvariables=("CGPATH"   \
    "DALTONPATH"   \
    "DEPOSITPATH"   \
    "DEPTOOLS"   \
    "DFTBPARAMETERS"   \
    "DFTBPATH"   \
    "HOSTFILE"   \
    "IBIPATH"   \
    "KMCDEPOSITPATH"   \
    "LD_LIBRARY_PATH"   \
    "LFPATH"   \
    "LOCAL"   \
    "LOCALCONDA"   \
    "MPI_PATH"   \
    "NANOMATCH"   \
    "NANOVER"   \
    "NM_LICENSE_SERVER"   \
    "OMP_NUM_THREADS"   \
    "OPENMMPATH"   \
    "OPENMPIPATH"    \
    "PATH"   \
    "PARNODES" \
    "PYTHONPATH"   \
    "SCRATCH"   \
    "SHREDDERPATH"   \
    "SIMONAPATH"   \
    "SLURM_CPU_BIND"   \
    "THREADFARMPATH"   \
    "TURBODIR"   \
    "UC_MEMORY_PER_NODE"   \
    "UC_NODES"   \
    "UC_PROCESSORS_PER_NODE"   \
    "UC_TOTAL_PROCESSORS"   \
    "UC_TOTAL_PROCESSORS"   \
    "TURBODIR"   \
    "TURBOMOLE_SYSNAME" \
    "XTBPATH"   )


ENVCOMMAND=""
for var in "${environmentvariables[@]}"
do
  if [ "$(varisset ${var})" == "true" ]
  then
        ENVCOMMAND="$ENVCOMMAND -x $var"
  fi
done

export DepositOpt="{{ wano["forcefield_optimization"]["train_set_generation"] }}"
if [ "$DepositOpt" == "from_deposit" ]
then
    mkdir deposit_input
    cd deposit_input
	unzip ../restartfile.zip
    gunzip deposited_*.gz
    cd ..
fi

echo "version: v4" >> rendered_wano.yml

# create output_dict for report
cp rendered_wano.yml output_dict.yml


mpirun --bind-to none $NMMPIARGS $ENVCOMMAND --hostfile $HOSTFILE --mca btl self,vader,tcp python -m mpi4py `which DihedralParametrizer` rendered_wano.yml >> mainout.txt 2> dhp_mpi_stderr

if [ "$DepositOpt" == "from_deposit" ]
then
    rm -rf deposit_input
fi

