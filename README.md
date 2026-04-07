# gFetch

![Version](https://img.shields.io/badge/version-0.10.2-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

gFetch is a simple and lightweight Python tool built around the [NCBI Datasets CLI](https://github.com/ncbi/datasets). It simplifies downloading and summarizing genomic, gene, and virus data from NCBI, and automatically switches to dehydrated download mode for large assemblies, with a threshold set on 10GB.

## Depedencies
### Python
gFetch requires python v.3.8+ and the requests package.

Install requests:
```bash
pip install requests
```
### NCBI Datasets CLI
Install datasets via conda:
```bash
conda install -c conda-forge ncbi-datasets-cli
```
Or follow the official instructions at [NCBI datatsets instructions](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/download-and-install/).

## Installation
Clone the repository and install depedencies:
```bash
git clone https://github.com/mikeph52/gfetch.git
```

## Usage
To run gfetch.py:
```bash
python gfetch.py
```

## Attribution
 
gFetch is built on the **NCBI Datasets** tool:
 
> O'Leary NA, Cox E, Holmes JB, Anderson WR, Falk R, Hem V, Tsuchiya MTN, Schuler GD, Zhang X, Torcivia J, et al. Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets. *Sci Data*. 2024 Jul 5;11(1):732. doi: 10.1038/s41597-024-03571-y.
 
NCBI Datasets is a product of the **National Center for Biotechnology Information (NCBI)**, National Library of Medicine, NIH.

## License
 
gFetch is released under the **MIT License**. You are free to use, modify, and distribute this software without restriction. See [LICENSE](LICENSE) for details.
 
The underlying NCBI Datasets CLI and data are subject to NCBI's own usage policies:
https://www.ncbi.nlm.nih.gov/home/about/policies/

## Changelog

### Version 0.10.2 4/4/2026
- First pre-release version.
- Fixed cli logic.
- Added summary for viruses.