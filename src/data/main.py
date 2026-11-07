from pathlib import Path

import config as cfg
import pandas as pd
from data_provider import DataProvider

# Load the data 
providers = [DataProvider(provider_name, quality_rules) for provider_name, quality_rules in cfg.provider_quality.items()]
for provider in providers:
    provider.load_data("./data/raw")
    provider.standardize_data()
    provider.validate_data()

# Write standardized and validated data
cleaned_provider_data = {
    provider.provider: provider.data
    for provider in providers
}

all_provider_data = pd.concat(
    cleaned_provider_data.values(),
    ignore_index=True
)
Path("./data/processed").mkdir(parents=True, exist_ok=True)
all_provider_data.to_csv("./data/processed/all_companies.csv", index=False)

# Generate a quality report
quality_report = pd.concat(
    [provider.generate_quality_report() for provider in providers]
)

quality_report.to_csv("./data/processed/provider_quality_report.csv")