# Bodium-OGS-Coupling

Coupling of the [Bodium python module](https://git.ufz.de/FINAM/bodium-module/-/blob/main/README.md) and the [OpenGeoSys python module](https://git.ufz.de/FINAM/finam-ogs6-module)

## Getting started (on EVE)

### FINAM OGS6 Python Component

See the [README.md](https://git.ufz.de/FINAM/finam-ogs6/-/blob/main/README.md).

### FINAM Bodium Module

See the [README.md](https://git.ufz.de/FINAM/bodium-module/-/blob/main/README.md).

### Coupling model

See [issue](https://git.ufz.de/landtrans/landtech/management/-/issues/224)

## Description

Coupling of the systemic soil model [Bodium](https://www.bonares.de/service-portal/models-concepts-evaluations/bodium-modell?locale=en&)
with groundwater model implemented in [OpenGeoSys](https://www.opengeosys.org).
The goal of the coupling was to show the distribution and transport of
furtilizer components in the groundwater.


## Usage

After the installation of Bodium, Bodium FINAM module, OGS, and OGS FINAM
component the simulation is started:

```
python BodiumOGS6Coupling.py
```

Simulation output will be written to a temporary directory in the `/tmp` folder.

## Support

Sara König <sara.koenig@ufz.de>
Thomas Fischer <thomas.fischer@ufz.de>

## Authors and acknowledgment

Sara König <sara.koenig@ufz.de>
Thomas Fischer <thomas.fischer@ufz.de>
Jeisson Javier Leal Rojas <jeisson-javier.leal-rojas@ufz.de>
Martin Lange <martin.lange@ufz.de>
Sebastian Müller <sebastian.mueller@ufz.de>
Stephan Thober <stephan.thober@ufz.de>
