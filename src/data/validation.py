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