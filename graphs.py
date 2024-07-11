import consts
import json
import os

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter



GRAPHS_PATH = "graphs"

def load_evaluation_metrics():
    with open(consts.EVALUATION_METRICS_NAME, "r") as f_in:
        data = json.loads(f_in)
    return data

def roc(metrics):
    ROC_GRAPH_NAME = "roc.png"

    far_list = []
    dir_list = []

    for threshold in metrics:
        threshold_metrics = metrics[threshold]
        far_list.append(threshold_metrics["FAR"])  
        dir_list.append(threshold_metrics["DIR"])  

    plt.figure()
    plt.plot(far_list, dir_list)
    plt.xlabel('False Acceptance Rate')
    plt.ylabel('Detect and Identify Rate')
    plt.title('ROC Curve')
    
    if not os.path.exists(GRAPHS_PATH):
        os.mkdir(GRAPHS_PATH)
    path = os.path.join(GRAPHS_PATH, ROC_GRAPH_NAME)
    plt.savefig(path)

def det(metrics):
    DET_GRAPH_NAME = "det.png"

    far_list = []
    frr_list = []

    for threshold in metrics:
        far_list.append(metrics[threshold]["FAR"])
        frr_list.append(metrics[threshold]["FRR"])

    plt.figure()
    plt.plot(far_list, frr_list)

    plt.xscale('log')
    plt.yscale('log')

    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:g}'.format(x)))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:g}'.format(y)))

    plt.xlabel('False Acceptance Rate')
    plt.ylabel('False Rejection Rate')
    plt.title('DET Curve')

    # Adjust layout to prevent label cropping
    plt.tight_layout()

    if not os.path.exists(GRAPHS_PATH):
        os.mkdir(GRAPHS_PATH)
    path = os.path.join(GRAPHS_PATH, DET_GRAPH_NAME)
    
    plt.savefig(path)

def eer(metrics):
    EER_GRAPH_NAME = "eer.png"

    frr_list = []
    far_list = []

    for threshold in metrics:
        far_list.append(metrics[threshold]["FAR"])
        frr_list.append(metrics[threshold]["FRR"])

    plt.figure()
    plt.plot(frr_list, label="FRR")
    plt.plot(far_list, label="FAR")
    plt.xlabel('Thresholds')
    plt.title('Watchlist Equal Error Rate')
    plt.legend()
    
    if not os.path.exists(GRAPHS_PATH):
        os.mkdir(GRAPHS_PATH)
    path = os.path.join(GRAPHS_PATH, EER_GRAPH_NAME)
    
    plt.savefig(path)


def generate_graphs():
    metrics = load_evaluation_metrics()

    if not metrics == dict():
        roc(metrics)
        det(metrics)
        eer(metrics)
