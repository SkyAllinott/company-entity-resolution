import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

generator = np.random.default_rng(seed = 4)
def generate_random_date(start_date, end_date, generator):
    time_between = end_date - start_date
    days_between = time_between.days

    random_number_days = int(generator.integers(low = 0, high = days_between + 1))

    return start_date + timedelta(days = random_number_days)

company_name_prefix = ["The", "A", "Canadian", "American", "English"]
company_name_words = ["Apple", "Micro", "Bloom", "Theory", "Red", "Orange", "Python", "Rust", "Ford", "Chevy", "Discord"]
company_name_suffix = ["Company", "Incorporated", "LLC", "inc.", "Limited", "Mutual", "Financial", "Consulting"]

# Potential operating countries
countries = ["United Kingdom", "England", "Canada", "United States", "US"]

# Potential industries
industry = ["Financials", "Technology", "Industrial", "Energy", "Health Care"]
def generate_companies(records, generator):
    data_list = []

    registration_ids = generator.choice(np.arange(1000, 100000), size = records, replace = False)
    for i in range(records):
        data_list.append({
            "company_id": f"COMP-{i + 1:05d}",
            "company_name": generator.choice(company_name_prefix) + " " + generator.choice(company_name_words),
            "country": generator.choice(countries),
            "registration_id": registration_ids[i],
            "industry": generator.choice(industry)
        })

    df = pd.DataFrame(data_list)
    file_path = Path("./data/raw/true company data.csv")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index = False)
    return df


def make_missing_records(missing_rate, df, generator, column):
    rows_to_make_missing = df.sample(frac = missing_rate, random_state = generator).index
    df.loc[rows_to_make_missing, str(column)] = np.nan

    return df


def add_company_suffix(fraction, df, generator):
    rows_to_add_suffix = df.sample(frac = fraction, random_state = generator).index
    df.loc[rows_to_add_suffix, "company_name"] = df.loc[rows_to_add_suffix, "company_name"] + " " + generator.choice(company_name_suffix, size = len(rows_to_add_suffix))

    return df


provider_quality = {
    "Envirotech": {
        "industry": 0.02,
        "registration_id": 0.05,
        "country": 0.05
    },
    "FinData": {
        "industry": 0.05,
        "registration_id": 0.15,
        "country": 0.1
    },
    "BigData": {
        "industry": 0.10,
        "registration_id": 0.1,
        "country": 0.2
    }
}


def generate_provider_data(provider, companies, generator):
    """Generate fake synthetic company entity data"""
    provider_companies = companies.sample(
        n = 800,
        random_state = generator
    )
    provider_companies.insert(
        0, 
        "provider_id", 
        provider + "-" + (np.arange(len(provider_companies)) + 1).astype(str)
    )

    provider_companies = provider_companies.drop(columns = "company_id")

    provider_companies = add_company_suffix(0.5, provider_companies, generator)


    # Make some randomly missing records. If provider is new, use BigData rates
    provider_miss_rates= provider_quality.get(provider, provider_quality["BigData"])

    for column, missing_rate in provider_miss_rates.items():
        provider_companies = make_missing_records(missing_rate, provider_companies, generator, column)

    file_path = Path("./data/raw/" + provider + " company data.csv")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    provider_companies.to_csv(file_path, index = False)
    return provider_companies

providers = ["Envirotech", "FinData", "BigData"]
actual_companies = generate_companies(1000, generator=generator)
for provider in providers:
    generate_provider_data(provider=provider, companies=actual_companies, generator=generator)