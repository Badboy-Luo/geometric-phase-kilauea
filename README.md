# geometric-phase-kilauea – Code Package

This repository contains the codes, parameter files, and example data supporting the study:

**"Geometric phase sensing using seismic waves: A new tool for comprehensive volcano monitoring at Kilauea, Hawaii"**  
(submitted to *Nature Communications*, 2025)

The package is organized into four major components reflecting the major analysis described in the paper:

1. **cross-correlation/** – MSNoise parameter files and scripts for preprocessing and ambient seismic noise cross-correlation.  
2. **eta/** – Custom Python code to calculate geometric phase changes (Δη) from cross-correlation functions (CCFs).  
3. **MFP/** – Custom Python code to estimate noise source energy distribution using matched field processing (MFP).  
4. **simulation/** – SPECFEM2D parameter files for numerical simulations for Δη.  


---

## Repository Structure

```
geometric-phase-kilauea/
│
├── cross_correlation/     # MSNoise parameter files and setup
├── eta/                   # Δη calculation code
├── mfp/                   # Matched field processing code
├── simulation/            # SPECFEM2D parameter files
├── software_versions.txt  # Software version specification
└── README.md              # This file
```
