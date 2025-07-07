import pandas as pd
from src.alpha.arima_filter import arima_signal
from src.alpha.features import build_feature_frame
from src.alpha.trainer import offline_train
from src.alpha.model import PumpClassifier
from src.network_analysis.clustering import louvain_clusters
from src.network_analysis.graph_builder import build_mst
from src.portfolio.representatives import pick_representatives


def test_alpha_and_network(tmp_path):
    prices = list(range(60))
    assert not arima_signal(prices, (1, 0, 0), 0.1)

    price_df = pd.DataFrame({"A": range(60), "B": range(60)})
    volume_df = pd.DataFrame({"A": range(60), "B": range(60)})
    feats = build_feature_frame(price_df, {"A": 0, "B": 1}, volume_df, {"A": 0.1, "B": 0.2})
    assert not feats.empty

    csv = tmp_path / "pumps.csv"
    df = pd.DataFrame({"x": [1], "is_pump": [0]})
    df.to_csv(csv, index=False)
    orig_fit = PumpClassifier.fit
    PumpClassifier.fit = lambda self, X, y: None
    offline_train(csv)
    PumpClassifier.fit = orig_fit

    corr = price_df.pct_change().dropna().corr()
    g = build_mst(corr)
    part = louvain_clusters(g)
    reps = pick_representatives(part, {s: 1.0 for s in part})
    assert isinstance(reps, list)
