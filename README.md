# FINAM Example Workflows

This repository provides the source code for the introductory example and three detailed workflows featured in the FINAM paper. These examples demonstrate how to set up, run, and analyze coupled environmental models using the FINAM framework.

## Repository Structure

```
.
├── 00_example_PET/
├── 01_workflow_toy_model/
├── 02_workflow_Bodium_OGS/
├── 03_workflow_regridding/
└── README.md
```

### 00_example_PET

A simple introductory example demonstrating the use of FINAM for calculating potential evapotranspiration (PET) with minimal setup.

### 01_workflow_toy_model

A minimalistic, synthetic coupled model example that demonstrates the coupling of two simple models exchanging time series data with bi-directional dependencies.

### 02_workflow_Bodium_OGS

A real-world coupled surface–subsurface workflow combining the Bodium model and OpenGeoSys (OGS), as presented in the FINAM paper.

### 03_workflow_regridding

A workflow showcasing advanced spatio-temporal regridding between models with different spatial and temporal discretizations using FINAM’s built-in regridding functionality.

---

## How to Use

1. **Clone the Repository**
   ```bash
   git clone https://github.com/finam-ufz/paper-workflows.git
   cd paper-workflows
   ```

2. **Explore the Folders**
   Each folder includes instructions (`README.md` or comments) for running the workflow and reproducing results.

3. **Dependencies**
   These examples require Python and the FINAM package. Please see the [FINAM documentation](https://finam.pages.ufz.de) for installation instructions.

---

## Citation

If you use these workflows or examples, please cite:

> Müller, S., Lange, M., Fischer, T., König, S., Kelbling, M., Leal Rojas, J. J., and Thober, S.:
> **FINAM – is not a model (v1.0): a new Python-based model coupling framework**,
> *Geosci. Model Dev. Discuss.* [preprint], https://doi.org/10.5194/gmd-2024-144, 2024.

---

## License

Distributed under the LGPL License. See **LICENSE** for more information.
