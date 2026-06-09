import pandas as pd


def compute_defense_awareness(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["slide_tackle", "stand_tackle", "interceptions"]

    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    data = df[cols].copy()

    null_counts = data.isnull().sum()
    if null_counts.any():
        data = data.fillna(data.median())

    normalized = (data - data.min()) / (data.max() - data.min()).replace(0, 1)

    corr = normalized.corr().abs()

    weights = corr.sum() - 1  # exclude self-correlation (diagonal = 1)
    weights /= weights.sum()

    df = df.copy()
    df["defense_awareness"] = (round(normalized.dot(weights) * 100)).clip(0,99).astype(int)

    return df