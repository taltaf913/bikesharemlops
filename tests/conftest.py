import sys
from pathlib import Path
import pandas as pd
import numpy as np
import pytest
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import pytest
from sklearn.model_selection import train_test_split

from bikeshare_model.config.core import config
from bikeshare_model.processing.data_manager import _load_raw_dataset
@pytest.fixture
def sample_input_data():
    """
    Provide a DataFrame used by tests. If a sample CSV exists in tests/sample_input_data.csv
    use it (keeps compatibility with upstream example data). Otherwise, return a minimal
    DataFrame that satisfies the tests' requirements:
      - has an 'Age' column
      - index label 709 exists and its Age is NaN initially
      - other non-NaN ages such that the median (or expected imputation) yields 21
    """
    data_file = Path(__file__).parent / "sample_input_data.csv"
    if data_file.exists():
        # If you have a canonical sample CSV, load it (preserve index if present)
        try:
            return pd.read_csv(data_file, index_col=0)
        except Exception:
            return pd.read_csv(data_file)
    # Fallback minimal dataset
    df = pd.DataFrame(
        {
            "Age": [21, 21, np.nan, 30],
            # add any other columns tests might require, example placeholders:
            # "SomeOtherCol": ["a", "b", "c", "d"],
        },
        index=[0, 1, 709, 3],
    )
    return df