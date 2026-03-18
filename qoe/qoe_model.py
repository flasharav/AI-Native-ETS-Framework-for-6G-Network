
import numpy as np
from scipy.special import expit          # Sigmoid function
from sklearn.preprocessing import MinMaxScaler


def latency_qoe(latency_ms, threshold=50):
    """
    Maps latency to QoE using a sigmoid decay model.

    Below threshold: high QoE
    Above threshold: sharp QoE degradation
    """
    a = 0.1  # steepness of degradation
    return 1.0 - expit(a * (latency_ms - threshold))



def throughput_qoe(throughput_mbps, max_throughput=100):
    """
    Maps throughput to QoE using logarithmic growth.
    Models diminishing returns at high throughput.
    """
    return np.log1p(throughput_mbps) / np.log1p(max_throughput)




def loss_qoe(packet_loss):
    """
    Maps packet loss to QoE using exponential decay.
    Small loss causes significant QoE degradation.
    """
    k = 5  # loss sensitivity constant
    return np.exp(-k * packet_loss)



def combined_qoe(latency, throughput, loss):
    """
    Combines individual QoE components using ITU-inspired weights.
    """
    q_lat = latency_qoe(latency)
    q_thr = throughput_qoe(throughput)
    q_loss = loss_qoe(loss)

    w_lat = 0.5
    w_thr = 0.3
    w_loss = 0.2

    return (w_lat * q_lat) + (w_thr * q_thr) + (w_loss * q_loss)



def qoe_to_mos(qoe_value):
    """
    Converts QoE (0–1) to MOS (1–5).
    """
    return 1.0 + 4.0 * qoe_value



def normalize_mos(mos):
    """
    Normalizes MOS to range 0–1 using MinMaxScaler.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    mos_array = np.array([[mos]])
    return scaler.fit_transform(mos_array)[0][0]


def compute_qoe(latency, throughput, loss):
    """
    Main Layer-2 function.
    Converts QoS metrics into normalized QoE score.
    """
    qoe_raw = combined_qoe(latency, throughput, loss)
    mos = qoe_to_mos(qoe_raw)
    qoe_normalized = normalize_mos(mos)
    return qoe_normalized


