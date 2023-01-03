import numpy as np
import bentoml
from bentoml.io import NumpyNdarray
from sklearn.preprocessing import PolynomialFeatures

lr_model_runner = bentoml.sklearn.get("ed_volume_model:latest").to_runner()

svc = bentoml.Service("ed_volume_model", runners=[lr_model_runner])

poly_feat = PolynomialFeatures(3)

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def predict(input_series: np.ndarray) -> np.ndarray:
    pred_abs = lr_model_runner.predict.run(poly_feat.fit_transform(np.array(range(24)).reshape(-1, 1)))
    pred_rel = pred_abs*100/sum(pred_abs)
    result = pred_rel * input_series
    result = np.array([round(x) for x in (pred_rel * input_series[0] / 100)])
    return result