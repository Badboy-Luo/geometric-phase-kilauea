# geometric-phase-kilauea – Code Package

This repository contains the codes, parameter files, and example data supporting the study:

**Luo, B., Beck, S., Deymier, P. et al. Geometric phase sensing using seismic waves for comprehensive volcano monitoring at Kı̄lauea Hawaii. Nature Communications (2026). https://doi.org/10.1038/s41467-026-73998-x**  

The package is organized into four major components reflecting the major analysis described in the paper:

1. **cross-correlation/** – MSNoise parameter files and scripts for preprocessing and ambient seismic noise cross-correlation.  
2. **eta/** – Custom Python code to calculate geometric phase changes (Δη) from example cross-correlation functions (CCFs).  
3. **MFP/** – Custom Python code to estimate noise source energy distribution using matched field processing (MFP).  
4. **simulation/** – SPECFEM2D parameter files for numerical simulations for Δη.  

## Example dataset
**We provide an example dataset of cross-correlation functions (CCFs) for review purposes**.  
Download link: [https://www.dropbox.com/scl/fi/ddnweorh0vijm0b8j1rtm/CCFs.zip?rlkey=o0csef8qsesl1rifr4zljbxv2&st=m1v8hjms&dl=0]  
- This dataset can be directly processed using the script `eta.py` located in the **eta/** folder.  
- Running this script with the example data will reproduce the 2018 Δη time series shown in Figure 2 of the manuscript.  

---

## Repository Structure

```
geometric-phase-kilauea/
│
├── cross_correlation/      # MSNoise parameter files and setup
├── eta/                    # Geometric phase (Δη) calculation code
├── MFP/                    # Matched field processing code
├── simulation/             # SPECFEM2D parameter files
├── dependencies.txt        # Software/libraries version specification
└── README.md               # This file
```
