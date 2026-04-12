# tests/test_size.py
"""
Size calculation and dehydrated download logic tests for gFetch.
Mocks subprocess calls to avoid real NCBI network requests.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from main import NCBIdownGenome, NCBIdownVirus


# ── Helpers ────────────────────────────────────────────────────────────────────

def make_summary_output(total_sequence_length):
    """Helper to generate a fake NCBI JSON Lines summary response."""
    record = {
        "assembly_stats": {
            "total_sequence_length": str(total_sequence_length)
        }
    }
    return json.dumps(record) + "\n"


def make_empty_summary_output():
    """Helper to generate a summary response with no assembly_stats."""
    return json.dumps({}) + "\n"


def make_multi_record_output(lengths):
    """Helper to generate multiple JSON Lines records."""
    lines = []
    for length in lengths:
        record = {"assembly_stats": {"total_sequence_length": str(length)}}
        lines.append(json.dumps(record))
    return "\n".join(lines) + "\n"


# ── Size Calculation ───────────────────────────────────────────────────────────

class TestSizeCalculation:

    def test_small_genome_uses_standard_download(self):
        """Genome under 10 GB should use standard download."""
        fake_stdout = make_summary_output(5_000_000_000)  # 5 GB

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownGenome("9606")

            # Second call is the download — check it does NOT use --dehydrated
            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" not in download_call

    def test_large_genome_uses_dehydrated_download(self):
        """Genome over 10 GB should use dehydrated download."""
        fake_stdout = make_summary_output(15_000_000_000)  # 15 GB

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownGenome("9606")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" in download_call

    def test_genome_exactly_10gb_uses_dehydrated(self):
        """Genome exactly at 10 GB threshold should use dehydrated download."""
        fake_stdout = make_summary_output(10_000_000_000)  # exactly 10 GB

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownGenome("9606")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" in download_call

    def test_missing_assembly_stats_defaults_to_standard_download(self):
        """Missing assembly_stats should default to 0 GB — standard download."""
        fake_stdout = make_empty_summary_output()

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownGenome("9606")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" not in download_call

    def test_multiple_records_summed_correctly(self):
        """Total size should be the sum of all records — triggers dehydrated if sum >= 10 GB."""
        # Two records of 6 GB each = 12 GB total → dehydrated
        fake_stdout = make_multi_record_output([6_000_000_000, 6_000_000_000])

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownGenome("9606")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" in download_call

    def test_multiple_small_records_no_dehydrated(self):
        """Multiple small records summing under 10 GB should use standard download."""
        # Three records of 1 GB each = 3 GB total → standard
        fake_stdout = make_multi_record_output([1_000_000_000, 1_000_000_000, 1_000_000_000])

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownGenome("9606")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" not in download_call

    def test_empty_stdout_does_not_crash(self):
        """Empty stdout from subprocess should not raise any exception."""
        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0)
            try:
                NCBIdownGenome("9606")
            except Exception as e:
                pytest.fail(f"NCBIdownGenome() raised an exception on empty stdout: {e}")


# ── Virus Size ─────────────────────────────────────────────────────────────────

class TestVirusSizeCalculation:

    def test_small_virus_uses_standard_download(self):
        """Virus dataset under 10 GB should use standard download."""
        fake_stdout = make_summary_output(1_000_000)  # 1 MB — typical virus

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownVirus("11676")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" not in download_call

    def test_large_virus_dataset_uses_dehydrated(self):
        """Virus dataset over 10 GB should use dehydrated download."""
        fake_stdout = make_summary_output(12_000_000_000)  # 12 GB

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownVirus("11676")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" in download_call

    def test_missing_assembly_stats_virus_defaults_to_standard(self):
        """Missing assembly_stats in virus record should default to standard download."""
        fake_stdout = make_empty_summary_output()

        with patch("main.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout=fake_stdout, returncode=0)
            NCBIdownVirus("11676")

            download_call = mock_run.call_args_list[1][0][0]
            assert "--dehydrated" not in download_call