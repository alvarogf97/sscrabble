import pytest
import tempfile
from pathlib import Path
from tools import config


def test_get_config_valid_file():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("access_token=my_secret_token\n")
        f.flush()
        f_path = f.name

    cfg = config.get_config(f_path)
    assert cfg.access_token == "my_secret_token"

    Path(f_path).unlink()


def test_get_config_missing_file():
    fake_path = "/tmp/non_existent_config_file"
    with pytest.raises(config.ConfigError) as exc:
        config.get_config(fake_path)
    assert "does not exists" in str(exc.value)


def test_get_config_invalid_format():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("not_a_valid_line_without_equal\n")
        f.flush()
        f_path = f.name

    with pytest.raises(config.ConfigError) as exc:
        config.get_config(f_path)
    assert "Impropery specified config file" in str(exc.value)

    Path(f_path).unlink()


def test_get_config_ignores_comments_and_blank_lines():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("# this is a comment\n\naccess_token =  abc123  \n")
        f.flush()
        f_path = f.name

    cfg = config.get_config(f_path)
    assert cfg.access_token == "abc123"

    Path(f_path).unlink()