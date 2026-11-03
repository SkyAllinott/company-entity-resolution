from datetime import datetime, timedelta
import numpy as np

"""
Contains all the variables needed to create the synthetic company data
"""

company_name_prefix = [
    "the", "a", "canadian", "american", "english"]
company_name_words = [
    "apple", "micro", "bloom", "theory", "red", "orange", "python", "rust", 
    "ford", "chevy", "discord", "macro", "anthropic", "intact", "aviva", "corsair",
    "nvidia", "tesla", "satellite", "google", "amazon", "hyper", "big one",
    "big business", "books", "brooks", "mcdonalds", "evil", "good", "unicorn",
    "paramount", "skydance", "bbc", "cbc", "nbc", "dc", "marvel",
    "lucas films", "a&w", "greggs"]
company_name_suffix = [
    "company", "incorporated", "llc", "inc.", "limited", "mutual", "financial", "consulting"]


# Potential operating countries
countries = [
    "united kingdom", "england", "uk", "scotland",
    "canada", "can", "ca",
    "united states", "us", "usa",
    "france", "fr", "fra"]


# Potential industries
industry = [
    "financials", "technology", "industrial", "energy", "health care"]


# Specific data quality aspects for each provider. 
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

def generate_random_date(start_date, end_date, generator):
    """Generate a random date"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_number_days = int(generator.integers(low = 0, high = days_between + 1))

    return start_date + timedelta(days = random_number_days)


def make_missing_records(missing_rate, df, generator, column):
    """Replace values in a column with NaN to simulate missing data"""
    rows_to_make_missing = df.sample(frac = missing_rate, random_state = generator).index
    df.loc[rows_to_make_missing, str(column)] = np.nan

    return df


def add_company_suffix(fraction, df, generator):
    """Generate company suffixes like 'inc.' to make names harder to distinguish from master"""
    rows_to_add_suffix = df.sample(frac = fraction, random_state = generator).index
    df.loc[rows_to_add_suffix, "company_name"] = df.loc[rows_to_add_suffix, "company_name"] + " " + generator.choice(company_name_suffix, size = len(rows_to_add_suffix))

    return df