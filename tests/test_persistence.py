from src.state import persistence


def test_save_and_load_state(tmp_path, monkeypatch):
    path = tmp_path / "state.joblib"
    monkeypatch.setattr(persistence, "_STATE", path)
    data = {"a": 1}
    persistence.save_state(data)
    assert path.exists()
    loaded = persistence.load_state()
    assert loaded == data


def test_load_state_missing(tmp_path, monkeypatch):
    path = tmp_path / "missing.joblib"
    monkeypatch.setattr(persistence, "_STATE", path)
    assert persistence.load_state() is None
