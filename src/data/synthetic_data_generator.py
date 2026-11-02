import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

import company_generator_variables as cv

generator = np.random.default_rng(seed = 4)
def generate_random_date(start_date, end_date, generator):
    """Generate a random date"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_number_days = int(generator.integers(low = 0, high = days_between + 1))

    return start_date + timedelta(days = random_number_days)


def generate_companies(records, generator):
    """Generate a master list of companies that serves as source of truth"""
    data_list = []

    registration_ids = generator.choice(np.arange(1000, 100000), size = records, replace = False)
    for i in range(records):
        data_list.append({
            "company_id": f"COMP-{i + 1:05d}",
            "company_name": (generator.choice(cv.company_name_prefix) + " " + generator.choice(cv.company_name_words)).title(),
            "country": (generator.choice(cv.countries)).title(),
            "registration_id": registration_ids[i],
            "industry": (generator.choice(cv.industry)).title()
        })

    df = pd.DataFrame(data_list)
    file_path = Path("./data/raw/true company data.csv")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index = False)
    return df


def make_missing_records(missing_rate, df, generator, column):
    """Replace values in a column with NaN to simulate missing data"""
    rows_to_make_missing = df.sample(frac = missing_rate, random_state = generator).index
    df.loc[rows_to_make_missing, str(column)] = np.nan

    return df


def add_company_suffix(fraction, df, generator):
    """Generate company suffixes like 'inc.' to make names harder to distinguish from master"""
    rows_to_add_suffix = df.sample(frac = fraction, random_state = generator).index
    df.loc[rows_to_add_suffix, "company_name"] = df.loc[rows_to_add_suffix, "company_name"] + " " + generator.choice(cv.company_name_suffix, size = len(rows_to_add_suffix))

    return df


def generate_provider_data(provider, companies, generator):
    """Sample the master data and introduce some poor data quality elements"""

    # From source of truth, sample some companies
    provider_companies = companies.sample(
        n = 800,
        random_state = generator
    )

    # Create the provider_id variable
    provider_companies.insert(
        0, 
        "provider_id", 
        provider + "-" + (np.arange(len(provider_companies)) + 1).astype(str)
    )

    # drop the company_id which is source of truth from provider (we're trying to match on this later) and alter company name
    provider_companies = provider_companies.drop(columns = "company_id")
    provider_companies = add_company_suffix(0.5, provider_companies, generator)


    # Make some randomly missing records. If provider is new, use BigData rates
    provider_miss_rates= cv.provider_quality.get(provider, cv.provider_quality["BigData"])
    for column, missing_rate in provider_miss_rates.items():
        provider_companies = make_missing_records(missing_rate, provider_companies, generator, column)

    file_path = Path("./data/raw/") / f"{provider} company data.csv"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    provider_companies.to_csv(file_path, index = False)
    return provider_companies


# Generate the synthetic data
providers = ["Envirotech", "FinData", "BigData"]
actual_companies = generate_companies(1000, generator=generator)
for provider in providers:
    generate_provider_data(provider=provider, companies=actual_companies, generator=generator)