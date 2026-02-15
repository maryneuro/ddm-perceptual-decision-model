from pathlib import Path

from ddm.cli import main


def test_cli_smoke_generates_plot(monkeypatch, tmp_path: Path) -> None:
    output_file = tmp_path / "smoke.png"
    monkeypatch.setattr(
        "sys.argv",
        [
            "ddm-sim",
            "--n-trials",
            "20",
            "--output",
            str(output_file),
        ],
    )

    main()

    assert output_file.exists()
    assert output_file.stat().st_size > 0
