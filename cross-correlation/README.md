# Cross-Correlation Module

This folder contains scripts and configuration files for computing ambient seismic noise cross-correlation using **MSNoise**.

## Contents
- `cc.sh` – Shell script to run MSNoise with the parameter settings used in the paper.
- `custom.py` – Python helper script loaded by `cc.sh`, used to read station information from `station`
- `station` – Station metadata in XML (FDSN StationXML). Used to get station information

## Usage
1. Install MSNoise (v1.6.3 recommended).
2. Download the required waveform data separately.
3. Run cross-correlation with:
   ```bash
   bash cc.sh

