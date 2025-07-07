from src.state.persistence import save_state, load_state


def test_state_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr("src.state.persistence._STATE", tmp_path / "state.json")
    save_state({"equity_curve": [1, 2, 3]})
    assert load_state() == {"equity_curve": [1, 2, 3]}


def test_state_invalid(tmp_path, monkeypatch):
    path = tmp_path / "state.json"
    path.write_text("not json")
    monkeypatch.setattr("src.state.persistence._STATE", path)
    assert load_state() is None
