import pandas as pd
from sklearn.metrics import f1_score
import numpy as np

data = pd.read_csv("data_patientB_80.csv", error_bad_lines=False)

y_true = data["Label"]
y_pred = data["detection"]

print(f1_score(y_true, y_pred))
