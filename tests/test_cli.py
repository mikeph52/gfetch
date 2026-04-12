# tests/test_cli.py
"""
CLI argument handling tests for gFetch.
Tests sys.argv parsing, command routing, and error handling.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from main import main, handle_download, handle_summary


# ── main() ────────────────────────────────────────────────────────────────────

class TestMain:

    def test_exits_when_no_args(self):
        """Should exit with code 1 when no arguments are provided."""
        with patch.object(sys, "argv", ["gfetch"]):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 1

    def test_exits_on_unknown_command(self):
        """Should exit with code 1 on an unknown command."""
        with patch.object(sys, "argv", ["gfetch", "invalidcmd"]):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 1

    def test_help_command_does_not_exit(self):
        """Help command should run without exiting."""
        with patch.object(sys, "argv", ["gfetch", "help"]):
            try:
                main()
            except SystemExit:
                pytest.fail("main() exited unexpectedly on help command")

    def test_download_command_routes_correctly(self):
        """Should call handle_download() when 'download' command is given."""
        with patch.object(sys, "argv", ["gfetch", "download", "-genome", "9606"]):
            with patch("main.startup"):
                with patch("main.handle_download") as mock_download:
                    main()
                    mock_download.assert_called_once()

    def test_summary_command_routes_correctly(self):
        """Should call handle_summary() when 'summary' command is given."""
        with patch.object(sys, "argv", ["gfetch", "summary", "-genome", "9606"]):
            with patch("main.startup"):
                with patch("main.handle_summary") as mock_summary:
                    main()
                    mock_summary.assert_called_once()


# ── handle_download() ─────────────────────────────────────────────────────────

class TestHandleDownload:

    def test_exits_when_too_few_args(self):
        """Should exit with code 1 when less than 4 args are given."""
        with patch.object(sys, "argv", ["gfetch", "download"]):
            with pytest.raises(SystemExit) as exc:
                handle_download()
            assert exc.value.code == 1

    def test_exits_on_unknown_data_type(self):
        """Should exit with code 1 on unknown data type like -xyz."""
        with patch.object(sys, "argv", ["gfetch", "download", "-xyz", "9606"]):
            with pytest.raises(SystemExit) as exc:
                handle_download()
            assert exc.value.code == 1

    def test_routes_genome(self):
        """Should call NCBIdownGenome() when -genome is specified."""
        with patch.object(sys, "argv", ["gfetch", "download", "-genome", "9606"]):
            with patch("main.NCBIdownGenome") as mock_fn:
                handle_download()
                mock_fn.assert_called_once_with("9606")

    def test_routes_gene(self):
        """Should call NCBIdownGene() when -gene is specified."""
        with patch.object(sys, "argv", ["gfetch", "download", "-gene", "9606"]):
            with patch("main.NCBIdownGene") as mock_fn:
                handle_download()
                mock_fn.assert_called_once_with("9606")

    def test_routes_virus(self):
        """Should call NCBIdownVirus() when -virus is specified."""
        with patch.object(sys, "argv", ["gfetch", "download", "-virus", "11676"]):
            with patch("main.NCBIdownVirus") as mock_fn:
                handle_download()
                mock_fn.assert_called_once_with("11676")


# ── handle_summary() ──────────────────────────────────────────────────────────

class TestHandleSummary:

    def test_exits_when_too_few_args(self):
        """Should exit with code 1 when less than 4 args are given."""
        with patch.object(sys, "argv", ["gfetch", "summary"]):
            with pytest.raises(SystemExit) as exc:
                handle_summary()
            assert exc.value.code == 1

    def test_exits_on_unknown_data_type(self):
        """Should exit with code 1 on unknown data type."""
        with patch.object(sys, "argv", ["gfetch", "summary", "-xyz", "9606"]):
            with pytest.raises(SystemExit) as exc:
                handle_summary()
            assert exc.value.code == 1

    def test_routes_genome(self):
        """Should call display_genome_summary() when -genome is specified."""
        with patch.object(sys, "argv", ["gfetch", "summary", "-genome", "9606"]):
            with patch("main.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"accession":"GCF_000001405.40","organism":{},"assembly_info":{},"assembly_stats":{}}\n',
                    returncode=0
                )
                with patch("main.display_genome_summary") as mock_display:
                    handle_summary()
                    mock_display.assert_called()

    def test_routes_gene(self):
        """Should call display_gene_summary() when -gene is specified."""
        with patch.object(sys, "argv", ["gfetch", "summary", "-gene", "4932"]):
            with patch("main.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"gene_id":851580,"symbol":"ACT1","taxname":"Saccharomyces cerevisiae","tax_id":4932}\n',
                    returncode=0
                )
                with patch("main.display_gene_summary") as mock_display:
                    handle_summary()
                    mock_display.assert_called()

    def test_routes_virus(self):
        """Should call display_virus_summary() when -virus is specified."""
        with patch.object(sys, "argv", ["gfetch", "summary", "-virus", "2697049"]):
            with patch("main.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    stdout='{"accession":"NC_045512.2","organism":{},"length":29903}\n',
                    returncode=0
                )
                with patch("main.display_virus_summary") as mock_display:
                    handle_summary()
                    mock_display.assert_called()