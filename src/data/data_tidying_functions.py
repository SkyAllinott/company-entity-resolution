import numpy as np
import re
import pandas as pd

def standardize_country(df, country_column):
    """Take in country mappings and standardize to known values. Does not handle what is an acceptable value, IE, a fake country. """
    country_mappings = {
        "uk": "united kingdom",
        "england": "united kingdom",
        "wales":"united kingdom",
        "scotland": "united kingdom",
        "us": "united states",
        "usa": "united states",
        "ca": "canada",
        "can": "canada",
        "fr": "france",
        "fra": "france"
    }

    df = df.copy()

    cleaned_col = df[country_column].astype("string").str.lower().str.strip().replace(country_mappings)
    df[country_column] = cleaned_col

    return df


def standardize_company_names(df, name_column):
    """Remove common superficial words in a company name such as 'LLC', 'company', etc."""
    words_to_remove = [
        "company", "incorporated", "llc", "inc", "limited", "mutual", "financial", "consulting"
    ]

    df = df.copy()

    # Remove . and , apply consistent lower case
    cleaned_col = df[name_column].astype("string").str.lower().str.strip().replace(r'[.,]', '', regex=True)

    # Remove the last word in the string if it matches words_to_remove
    company_suffix_pattern = r"\s+(?:" + "|".join(re.escape(word) for word in words_to_remove) + r")$"
    cleaned_col = cleaned_col.replace(company_suffix_pattern, "", regex = True)

    # Collapse whitespace
    cleaned_col = cleaned_col.replace(r"\s+", " ", regex = True)
    df[name_column] = cleaned_col

    return df


def validate_country(df, country_column):
    valid_countries = [
        "united states",
        "united kingdom",
        "canada", 
        "france"
    ]

    df = df.copy()

    # Check if the standardized country is in valid country list and create bool columns 
    df["country_is_missing"] = df[country_column].isna()
    df["country_is_valid"] = df[country_column].isin(valid_countries)
    df["country_is_invalid"] = (~df["country_is_valid"] & ~df["country_is_missing"])

    return df


def generate_quality_report(providers):
    data_quality = {}

    for provider in providers:
        data_quality_metrics = {}
        data = providers.get(provider)

        valid_countries_rate = (data["country_is_valid"].mean())
        missing_countries_rate = (data["country_is_missing"].mean())
        invalid_countries_rate = (data["country_is_invalid"].mean())

        data_quality_metrics["valid_countries_rate"] = valid_countries_rate
        data_quality_metrics["missing_countries_rate"] = missing_countries_rate
        data_quality_metrics["invalid_countries_rate"] = invalid_countries_rate
        data_quality[provider] = data_quality_metrics

    df = pd.DataFrame(data_quality)

    return df