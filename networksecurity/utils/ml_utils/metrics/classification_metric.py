from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import ClassifactionMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score
import sys


def get_classifaction_score(y_true,y_pred)->ClassifactionMetricArtifact:
    try:
        model_f1_score=f1_score(y_pred=y_pred,y_true=y_true)
        model_precision_score=precision_score(y_pred=y_pred,y_true=y_true)
        model_recall_score=recall_score(y_pred=y_pred,y_true=y_true)
        classification_metric_artifact:ClassifactionMetricArtifact=ClassifactionMetricArtifact(
            precision_score=model_precision_score,
            recall_score=model_recall_score,
            f1_score=model_f1_score
        )
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)