# gFetch

![Version](https://img.shields.io/badge/version-0.11.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

<img width="912" height="740" alt="Image" src="https://github.com/user-attachments/assets/5c1b92ef-e5ba-4ced-9c3d-4e0c4d9e04ce" />

gFetch is a simple and lightweight Python tool built around the [NCBI Datasets CLI](https://github.com/ncbi/datasets). It simplifies downloading and summarizing genomic, gene, and virus data from NCBI, and automatically switches to dehydrated download mode for large assemblies, with a threshold set on 10GB.

> [!NOTE]
> _If you have any suggestions for new features or a bug encountered, create an Issue or send me a message at: mikeph526@outlook.com. I'm happy to help._

## Depedencies
### Python
gFetch requires python v.3.8+ and the following packages.

Install packages:
```bash
pip install requests rich
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
Usage:
```bash
gfetch [mode] [type]-genome/-gene/-virus <taxon>
```
**Modes:** download/summary

**Types:** -genome/-gene/-virus

Currently, gfetch only supports the ncbi taxon numbers, the accesion number feature will be added in the next updates.

### Download mode
**For genomes**, when the download size surpasses the 10GB limit, the .zip file will be downloaded as a dehydrated file. The size limit was set after a lot experimentation with the ncbi datasets cli.

There's also an option to download only the reference genomes from selected taxons.

### Summary mode
In the summary mode, gfetch uses a Terminal User Interface (TUI) to display features extracted from the json file datasets generates. An example of the organism _Zootermopsis nevadensis_ is featured bellow:

```bash
             Genomic Summary
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Field        ┃ Value                   ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Organism     │ Zootermopsis nevadensis │
│ Taxon ID     │ 136037                  │
│ Accession    │ GCF_000696155.1         │
│ Assembly     │ ZooNev1.0               │
│ Level        │ Scaffold                │
│ Release Date │ 2014-07-22              │
└──────────────┴─────────────────────────┘
```

**For genomes**, an option to display only the summaries of the reference genomes from selected taxons is available.

## Attribution
 
gFetch is built on the **NCBI Datasets** tool:
 
> O'Leary NA, Cox E, Holmes JB, Anderson WR, Falk R, Hem V, Tsuchiya MTN, Schuler GD, Zhang X, Torcivia J, et al. Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets. *Sci Data*. 2024 Jul 5;11(1):732. doi: 10.1038/s41597-024-03571-y.
 
NCBI Datasets is a product of the **National Center for Biotechnology Information (NCBI)**, National Library of Medicine, NIH.

## License
 
gFetch is released under the **MIT License**. You are free to use, modify, and distribute this software without restriction. See [LICENSE](LICENSE) for details.
 
The underlying NCBI Datasets CLI and data are subject to NCBI's own [usage policies](https://www.ncbi.nlm.nih.gov/home/about/policies/):


## Changelog

### Version 0.11.0 8/4/2026
- Added a Terminal User Interface (TUI) in summary function using `rich`.
- Added option for reference genomes in download mode.
- Help funtion fixed.

### Version 0.10.2 4/4/2026
- First pre-release version.
- Fixed cli logic.
- Added summary for viruses.