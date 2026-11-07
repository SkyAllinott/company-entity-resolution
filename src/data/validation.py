def validate_country(df, country_column):
    valid_countries = ["united states", "united kingdom", "canada", "france"]

    df = df.copy()

    # Check if the standardized country is in valid country list and create bool columns
    df["country_is_missing"] = df[country_column].isna()
    df["country_is_valid"] = df[country_column].isin(valid_countries)
    df["country_is_invalid"] = ~df["country_is_valid"] & ~df["country_is_missing"]

    return df


def validate_registration(df, registration_column):
    df = df.copy()

    df["registration_missing"] = df[registration_column].isna()

    registration_ids = df[registration_column].dropna()
    unique_ids = ~registration_ids.duplicated(keep=False)
    df["registration_uniqueness"] = unique_ids.mean()

    return df


def validate_company_name(df, company_column):
    df = df.copy()

    df["company_missing"] = df[company_column].isna()

    company_names = df[company_column].dropna()
    unique_names = ~company_names.duplicated(keep=False)
    df["company_uniqueness"] = unique_names.mean()

    return df
