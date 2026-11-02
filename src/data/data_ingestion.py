import pandas as pd
from pathlib import Path
import data_tidying_functions as dt

def read_provider_data(providers, input_directory):
    provider_data = {}
    for provider in providers:
        provider_filepath = Path(input_directory) / f"{provider} company data.csv"

        try:
            provider_data[provider] = pd.read_csv(provider_filepath)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find data file for provider: {provider}"
            )

    return provider_data

providers = ["BigData", "Envirotech", "FinData"]
provider_data = read_provider_data(providers=providers, input_directory="./data/raw")

# Apply standardization to company's home country and company name 
standardized_provider_data = {
    provider: dt.standardize_country(df, "country")
    for provider, df in provider_data.items()}

standardized_provider_data = {
    provider: dt.standardize_company_names(df, "company_name")
    for provider, df in standardized_provider_data.items()
}

standardized_provider_data = {
    provider: dt.validate_country(df, "country")
    for provider, df in standardized_provider_data.items()
}


print(dt.generate_quality_report(providers=standardized_provider_data))