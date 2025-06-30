# Spatio-temporal Regridding Workflow

This workflow demonstrates the spatio-temporal regridding capabilities of the FINAM framework. It illustrates how to transform data between models with different spatial and temporal resolutions, while preserving the integrity of the data and minimizing the configuration burden on the user.

## Overview

Regridding is a fundamental operation in spatial data analysis, used to transfer data between different grids or coordinate systems. In environmental model coupling, this is essential for ensuring compatibility between models with different spatial resolutions or grid types.

FINAM provides built-in adapters for regridding and time averaging. The regridding operation can use linear or nearest-neighbor interpolation, as well as advanced methods via the `finam-regrid` package, which wraps the ESMF regridding algorithms. FINAM supports both structured and unstructured grids and automatically handles transformations between different coordinate reference systems (CRS).

## What This Workflow Does

- **Input:** A five-year time series of daily precipitation data on an **unstructured grid** (cell size ~0.5 km).
- **Process:**
  - Spatial regridding of daily data to a **regular target grid** with 1 km cells, covering a 5 x 4 km area.
  - Temporal aggregation: The regridded daily data is averaged into 30-day means.
- **Output:** 30-day mean precipitation on the regular grid, written to NetCDF format.

The workflow makes use of the following FINAM modules:
- `finam-vtk` to read unstructured time series data in PVD format.
- Built-in or `finam-regrid` adapters to perform conservative spatial regridding (preserving the total precipitation).
- Temporal averaging adapters to produce rolling means.
- `finam-netcdf` to write the output.

The adapters automatically detect the required grid specifications and time-stepping from the connected components, making the configuration straightforward and robust.

## Key Features

- **Automatic CRS Handling:** FINAM performs coordinate transformations automatically when source and target grids have different CRSs.
- **Minimal Configuration:** The adapters infer required information from the connected reader/writer components, avoiding manual errors.
- **Advanced Regridding:** Use of ESMF (via `finam-regrid`) enables conservative regridding for quantity preservation and supports structured and unstructured grids.
- **Dynamic Time Averaging:** Time averaging is configured to use the appropriate window based on the workflow setup; here, a 30-day rolling mean is computed.
- **Flexible Data Streams:** The workflow is easily integrated into larger coupled systems, e.g., for downstream crop yield estimation or further climate model coupling.

## Example Application

This example uses daily precipitation data from an unstructured grid, regrids it spatially to a 1 km regular grid, and aggregates it temporally to 30-day means. The process demonstrates how FINAM can be used to connect components operating on different spatio-temporal scales with minimal user effort.

A typical use case might be transferring meteorological output from an atmospheric model (daily, unstructured) to a crop model (monthly, regular grid), but the workflow is general and can be adapted to other scenarios.

## Further Information

- For more details on regridding methods, see the [finam-regrid documentation](https://finam.pages.ufz.de/finam-regrid).
- For an in-depth explanation of the underlying algorithms, refer to the FINAM paper and cited ESMF documentation.

## Citation

If you use this workflow, please cite:

> Müller, S., Lange, M., Fischer, T., König, S., Kelbling, M., Leal Rojas, J. J., and Thober, S.:
> **FINAM – is not a model (v1.0): a new Python-based model coupling framework**,
> *Geosci. Model Dev. Discuss.* [preprint], https://doi.org/10.5194/gmd-2024-144, 2024.

---

For questions, see the [main FINAM documentation](https://finam.pages.ufz.de) or contact the authors.
