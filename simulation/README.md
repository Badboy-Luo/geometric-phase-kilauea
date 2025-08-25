# SPECFEM2D Simulation

This folder contains the parameter files used for **SPECFEM2D** numerical modeling of geometric phase (Δη) for the reference time step with the initial velocity structure.

## Files
- `DATA`:
    - `Par_file` – Main SPECFEM2D parameter file (mesh size, time step, simulation duration, etc.).  
    - `SOURCES` – Defines the seismic sources used in the simulation (location, amplitude, type).  
    - `STATIONS` – Defines the receiver stations for synthetic wavefield recording.  
    - `interface.dat` – Defines layer interfaces in the velocity model.  
    - `tomo.dat` – Defines tomographic parameters include the initial velocity structure (serves as the reference time step for Δη simulation).
- `run.sh` - This script automates the SPECFEM2D simulation.

## Requirements
- SPECFEM2D v8.1.0  
- MPI-enabled Linux system for parallel computation 

## Usage
1. Download **SPECFEM2D** from the official repository: https://github.com/geodynamics/specfem2d
2. Compile following their installation guide. After compilation, the binaries `xmeshfem2D` and `xspecfem2D` should be available in a `bin/` directory.
3. Run the simulation.
    - Copy `run.sh` into the top-level SPECFEM2D directory (same level as `bin/` and `DATA/`).
    - ```bash
        bash run.sh

