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