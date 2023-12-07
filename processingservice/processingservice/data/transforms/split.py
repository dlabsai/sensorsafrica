import pandas as pd
from sklearn.model_selection import train_test_split


def dataset_random_split(df: pd.DataFrame, test_size: float) -> tuple:
    x = df.drop("value", axis=1)
    y = df["value"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=42
    )

    return x_train, x_test, y_train, y_test
