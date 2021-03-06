# -*- coding: utf-8 -*-
"""
    Tests for volt init command
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012-2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import os
from pathlib import Path

import yaml
from click.testing import CliRunner

from volt.cli import main
from volt.config import DEFAULT_CONFIG as DC


CFG_NAME = DC["volt"]["config_name"]


def test_init_default():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        wp = Path(fs)

        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0
        # Expected 3 items: contents dir, templates dir, config
        assert len(list(wp.iterdir())) == 3
        assert wp.joinpath(DC["volt"]["contents_path"]).exists()
        assert wp.joinpath(DC["volt"]["templates_path"]).exists()
        assert wp.joinpath(DC["volt"]["assets_path"]).exists()
        cfg_path = wp.joinpath(CFG_NAME)
        assert cfg_path.exists()
        # Config must be valid YAML
        with open(str(cfg_path), "r") as src:
            assert yaml.load(src)


def test_init_nonwritable_dir():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        os.chmod(fs, 0o555)
        wp = Path(fs)

        result = runner.invoke(main, ["init"])
        assert result.exit_code != 0
        assert isinstance(result.exception, SystemExit)
        assert "Error: Directory '{0}' is not writable.".format(wp) in \
            result.output


def test_init_nonempty():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        wp = Path(fs)
        exst_file = wp.joinpath("existing")
        exst_file.write_text("boom")

        result = runner.invoke(main, ["init"])
        assert result.exit_code != 0
        assert isinstance(result.exception, SystemExit)
        # Expected only 1 item: the preexisting file
        assert list(wp.iterdir()) == [exst_file]


def test_init_nonempty_with_force():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        wp = Path(fs)
        exst_file = wp.joinpath("existing")
        exst_file.write_text("boom")

        result = runner.invoke(main, ["init", "-f"])
        assert result.exit_code == 0
        # Expected 4 items: contents dir, templates dir, config, and the file
        wp_contents = list(wp.iterdir())
        assert len(wp_contents) == 4
        assert exst_file.exists()
        assert wp.joinpath(DC["volt"]["contents_path"]).exists()
        assert wp.joinpath(DC["volt"]["templates_path"]).exists()
        assert wp.joinpath(DC["volt"]["assets_path"]).exists()
        cfg_path = wp.joinpath(DC["volt"]["config_name"])
        assert cfg_path.exists()
        # Config must be valid YAML
        with open(str(cfg_path), "r") as src:
            assert yaml.load(src)


def test_init_with_config_samedir():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        wp = Path(fs)
        cfg = {"site": {"name": "test", "url": "http://test.com"}}
        cfg_path = wp.joinpath(CFG_NAME)
        cfg_s = yaml.dump(cfg, default_flow_style=False)
        cfg_path.write_text(cfg_s)

        result = runner.invoke(main, ["init", "-c", str(cfg_path)])
        assert result.exit_code == 0
        # Expected 4 items: contents dir, templates dir, config
        wp_contents = list(wp.iterdir())
        assert len(wp_contents) == 3
        assert cfg_path.exists()
        assert wp.joinpath(DC["volt"]["contents_path"]).exists()
        assert wp.joinpath(DC["volt"]["templates_path"]).exists()
        assert wp.joinpath(DC["volt"]["assets_path"]).exists()
        assert cfg_path.exists()
        # Config must be the same as expected
        with open(str(cfg_path), "r") as src:
            written = yaml.load(src)
            assert written == cfg


def test_init_with_config_samedir_nonexistent():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        wp = Path(fs)

        result = runner.invoke(main, ["init", "-c", "nope.yaml"])
        assert result.exit_code != 0
        assert isinstance(result.exception, SystemExit)
        # Expected no items
        assert not list(wp.iterdir())


def test_init_with_config_samedir_invalid():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        wp = Path(fs)
        cfg_path = wp.joinpath(CFG_NAME)
        cfg_path.write_text("invalid: 'yaml")

        result = runner.invoke(main, ["init", "-c", str(cfg_path)])
        assert result.exit_code != 0
        assert isinstance(result.exception, SystemExit)
        # Expected only the invalid config
        assert list(wp.iterdir()) == [cfg_path]
        assert "Error: Config contains syntax errors." in result.output


def test_init_with_config_samedir_unexpected():
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        wp = Path(fs)
        cfg_path = wp.joinpath(CFG_NAME)
        cfg_path.write_text("this is valid but unexpected")

        result = runner.invoke(main, ["init", "-c", str(cfg_path)])
        assert result.exit_code != 0
        assert isinstance(result.exception, SystemExit)
        # Expected only the invalid config
        assert list(wp.iterdir()) == [cfg_path]
        assert "Error: Unexpected config structure." in result.output
