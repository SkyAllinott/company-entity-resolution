import re

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