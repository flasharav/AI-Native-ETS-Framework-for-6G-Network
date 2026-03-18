import pandas as pd

def load_metrics(path):
    df = pd.read_csv(path)
    return {
        "latency": df["latency"].mean(),
        "throughput": df["throughput"].mean(),
        "loss": df["loss"].mean(),
        "traffic": df["traffic"].mean()
    }
