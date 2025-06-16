from src.agent.meta_controller import MetaController

def test_meta(tmp_path):
    mc = MetaController(tmp_path/"x.jsonl")
    mc.evaluate()  # no crash on empty
