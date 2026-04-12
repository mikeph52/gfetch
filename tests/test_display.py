import pytest
from main import display_genome_summary, display_gene_summary, display_virus_summary

# ── Genome ──────────────────────────────────────────────

def test_genome_summary_complete():
    """Should render without errors when all fields present."""
    data = {
        "accession": "GCF_000001405.40",
        "organism": {"organism_name": "Homo sapiens", "tax_id": 9606},
        "assembly_info": {
            "assembly_name": "GRCh38.p14",
            "assembly_level": "Chromosome",
            "release_date": "2022-02-03"
        },
        "assembly_stats": {
            "total_sequence_length": "3100000000",
            "gc_percent": 41.0
        }
    }
    display_genome_summary(data)   # should not raise


def test_genome_summary_missing_fields():
    """Should not crash when fields are missing."""
    display_genome_summary({})     # empty dict — all fields missing


# ── Gene ────────────────────────────────────────────────

def test_gene_summary_complete():
    data = {
        "gene_id": 851580,
        "symbol": "ACT1",
        "description": "actin",
        "taxname": "Saccharomyces cerevisiae",
        "tax_id": 4932,
        "common_name": "baker's yeast",
        "chromosomes": ["10"],
        "type": "PROTEIN_CODING"
    }
    display_gene_summary(data)


def test_gene_summary_missing_fields():
    display_gene_summary({})


# ── Virus ───────────────────────────────────────────────

def test_virus_summary_complete():
    data = {
        "accession": "NC_045512.2",
        "organism": {"organismName": "SARS-CoV-2", "taxId": 2697049},
        "length": 29903,
        "molType": "ssRNA(+)",
        "isAnnotated": True,
        "isolate": {"name": "Wuhan-Hu-1", "collectionDate": "2019-12"},
        "location": {"geographicLocation": "China", "geographicRegion": "Asia"}
    }
    display_virus_summary(data)


def test_virus_summary_missing_organism():
    """Should not crash when organism block is missing."""
    display_virus_summary({"accession": "NC_045512.2"})


def test_virus_summary_empty():
    display_virus_summary({})