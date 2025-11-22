# download-MARS

This repository provides example Python scripts for downloading **ERA5** data from **ECMWF MARS**.  
These scripts are simple templates that can be run directly or modified for your own needs.

## Scripts

### 1. `download_var_an.py`
Downloads ERA5 **analysis (AN)** fields (e.g., sp, msshf)

### 2. `download_var_fc.py`
Downloads ERA5 **forecast (FC)** fields. The script automatically:
- Selects the correct forecast cycle (**06 UTC** or **18 UTC**)  
- Computes the forecast step for the target hour  

## Requirements

- Python 3  
- `cdsapi` library  
- A configured `~/.cdsapirc` file (same as CDS API key)
