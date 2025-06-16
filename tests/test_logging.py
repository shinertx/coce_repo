import logging, json
from src.utils.logging_utils import JsonlFormatter

def test_json():
    rec = logging.LogRecord("m", logging.INFO, "", 0, "ok", None, None)
    j = JsonlFormatter().format(rec)
    json.loads(j)
