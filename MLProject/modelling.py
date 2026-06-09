import os
import argparse
import warnings
import json
import pickle
import pandas as pd
import mlflow
import mlflow.sklearn
import shutil
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
)
warnings.filterwarnings("ignore")


def parse_args():
    parser = argparse.ArgumentParser(description="Crop Recommendation — RF Training")
    parser.add_argument("--data_path",         type=str,   default="crop_recommendation_preprocessing/crop_recommendation_preprocessing.csv")
    parser.add_argument("--target_col",        type=str,   default="label_encoded")
    parser.add_argument("--test_size",         type=float, default=0.2)
    parser.add_argument("--random_state",      type=int,   default=42)
    parser.add_argument("--n_estimators",      type=str,   default="[100,200]")
    parser.add_argument("--max_depth",         type=str,   default="[null,10,20]")
    parser.add_argument("--min_samples_split", type=str,   default="[2,5]")
    parser.add_argument("--cv_folds",          type=int,   default=5)
    return parser.parse_args()


def load_data(data_path, target_col):
    print(f"[INFO] Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"[INFO] Shape: {df.shape}")
    print(f"[INFO] Columns: {df.columns.tolist()}")

    drop_cols = [target_col, "label"] if "label" in df.columns else [target_col]
    X = df.drop(columns=drop_cols)
    y = df[target_col]

    print(f"[INFO] Features: {X.columns.tolist()}")
    print(f"[INFO] Target  : {target_col}  |  Classes: {sorted(y.unique())}")
    return X, y


def run_training(args):
    X, y = load_data(args.data_path, args.target_col)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )
    print(f"[INFO] Train size: {len(X_train)}  |  Test size: {len(X_test)}")

    param_grid = {
        "n_estimators":      json.loads(args.n_estimators),
        "max_depth":         json.loads(args.max_depth),
        "min_samples_split": json.loads(args.min_samples_split),
    }
    print(f"[INFO] Param grid: {param_grid}")

    mlflow.log_param("test_size",    args.test_size)
    mlflow.log_param("random_state", args.random_state)
    mlflow.log_param("cv_folds",     args.cv_folds)
    mlflow.log_param("param_grid",   str(param_grid))

    print("[INFO] Running GridSearchCV ...")
    base_rf = RandomForestClassifier(random_state=args.random_state, n_jobs=-1)
    grid_search = GridSearchCV(
        estimator=base_rf,
        param_grid=param_grid,
        cv=args.cv_folds,
        scoring="accuracy",
        n_jobs=-1,
        verbose=1,
    )
    grid_search.fit(X_train, y_train)

    best_model  = grid_search.best_estimator_
    best_params = grid_search.best_params_
    print(f"[INFO] Best params: {best_params}")

    for k, v in best_params.items():
        mlflow.log_param(f"best_{k}", v)

    y_pred    = best_model.predict(X_test)
    acc       = accuracy_score(y_test, y_pred)
    f1        = f1_score(y_test, y_pred, average="weighted")
    precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    recall    = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring="accuracy")

    print(f"\n[RESULT] Accuracy  : {acc:.4f}")
    print(f"[RESULT] F1 Score  : {f1:.4f}")
    print(f"[RESULT] Precision : {precision:.4f}")
    print(f"[RESULT] Recall    : {recall:.4f}")
    print(f"[RESULT] CV Mean   : {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")

    mlflow.log_metric("accuracy",         acc)
    mlflow.log_metric("f1_score",         f1)
    mlflow.log_metric("precision",        precision)
    mlflow.log_metric("recall",           recall)
    mlflow.log_metric("cv_mean_accuracy", cv_scores.mean())
    mlflow.log_metric("cv_std_accuracy",  cv_scores.std())
    mlflow.log_metric("best_cv_score",    grid_search.best_score_)

    report = classification_report(y_test, y_pred)
    print("\n[REPORT]\n", report)
    with open("classification_report.txt", "w") as f:
        f.write(report)
    mlflow.log_artifact("classification_report.txt")

    cm_df = pd.DataFrame(confusion_matrix(y_test, y_pred))
    cm_df.to_csv("confusion_matrix.csv", index=False)
    mlflow.log_artifact("confusion_matrix.csv")

    mlflow.log_artifact(args.data_path)

    mlflow.sklearn.log_model(
        sk_model=best_model,
        artifact_path="random_forest_model",
        registered_model_name="crop-recommendation-rf",
    )

    if os.path.exists("model_output"):
        shutil.rmtree("model_output")

    mlflow.sklearn.save_model(
    sk_model=best_model,
    path="model_output",
    )
    print("[INFO] MLflow model saved to model_output/")
    mlflow.log_artifact("model_output")

    run_id = mlflow.active_run().info.run_id
    with open("run_id.txt", "w") as f:
        f.write(run_id)
    print(f"[INFO] run_id saved to run_id.txt: {run_id}")
    print(f"\n[DONE] Training completed. run_id: {run_id}")


if __name__ == "__main__":
    args = parse_args()

    injected_run_id = os.environ.get("MLFLOW_RUN_ID", "").strip()

    if injected_run_id:
        print(f"[INFO] MLflow Project mode — resuming run: {injected_run_id}")
        with mlflow.start_run():
            run_training(args)
    else:
        print("[INFO] Standalone mode — creating new MLflow run")
        mlflow.set_experiment("crop-recommendation-rf")
        with mlflow.start_run():
            run_training(args)