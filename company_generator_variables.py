company_name_prefix = ["The", "A", "Canadian", "American", "English"]
company_name_words = ["Apple", "Micro", "Bloom", "Theory", "Red", "Orange", "Python", "Rust", "Ford", "Chevy", "Discord"]
company_name_suffix = ["Company", "Incorporated", "LLC", "inc.", "Limited", "Mutual", "Financial", "Consulting"]

# Potential operating countries
countries = ["United Kingdom", "England", "Canada", "United States", "US"]

# Potential industries
industry = ["Financials", "Technology", "Industrial", "Energy", "Health Care"]

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