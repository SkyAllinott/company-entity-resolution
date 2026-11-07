from pathlib import Path

import config as cfg
import numpy as np
import pandas as pd
import standardization as stan
import validation as val


class DataProvider:
    def __init__(self, provider, quality_rules=cfg.provider_quality):
        self.provider = provider
        self.quality_rules = quality_rules
        self.data = None

    def generate_reference_data(self, generator, records: int):
        """Generate a master list of companies that serves as source of truth"""
        data_list = []

        registration_ids = generator.choice(
            np.arange(1000, 100000), size=records, replace=False
        )
        for i in range(records):
            data_list.append(
                {
                    "company_id": f"COMP-{i + 1:05d}",
                    "company_name": (
                        generator.choice(cfg.company_name_prefix)
                        + " "
                        + generator.choice(cfg.company_name_words)
                    ).title(),
                    "country": (generator.choice(cfg.countries)).title(),
                    "registration_id": registration_ids[i],
                    "industry": (generator.choice(cfg.industry)).title(),
                }
            )

        df = pd.DataFrame(data_list)
        file_path = Path("./data/raw/true company data.csv")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)

        return df

    def generate_provider_data(self, companies, generator):
        """Sample the master data and introduce some poor data quality elements"""
        # From source of truth, sample some companies
        provider_companies = companies.sample(n=800, random_state=generator)

        # Create the provider_id variable
        provider_companies.insert(
            0,
            "provider_id",
            self.provider + "-" + (np.arange(len(provider_companies)) + 1).astype(str),
        )

        # drop the company_id which is source of truth from provider (we're trying to match on this later) and alter company name
        provider_companies = provider_companies.drop(columns="company_id")
        provider_companies = cfg.add_company_suffix(0.5, provider_companies, generator)

        # Make some randomly missing records. If provider is new, use BigData rates
        provider_quality = self.quality_rules
        provider_miss_rates = provider_quality.get(
            self.provider, provider_quality.get("BigData")
        )
        for column, missing_rate in provider_miss_rates.items():
            provider_companies = cfg.make_missing_records(
                missing_rate, provider_companies, generator, column
            )

        file_path = Path("./data/raw/") / f"{self.provider} company data.csv"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        provider_companies.to_csv(file_path, index=False)
        return provider_companies

    def load_data(self, input_directory):
        provider_filepath = Path(input_directory) / f"{self.provider} company data.csv"

        try:
            self.data = pd.read_csv(provider_filepath)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find data file for provider: {self.provider}"
            )

        return self.data

    def standardize_data(self):
        # Apply standardization to company's home country and company name
        if self.data is None:
            raise ValueError(f"No data loaded for provider: {self.provider}")

        self.data = stan.standardize_country(self.data, "country")
        self.data = stan.standardize_company_names(self.data, "company_name")

        return self.data

    def validate_data(self):
        if self.data is None:
            raise ValueError(
                f"No data loaded and standardized for provider: {self.provider}"
            )

        self.data = val.validate_country(self.data, "country")
        self.data = val.validate_registration(self.data, "registration_id")
        self.data = val.validate_company_name(self.data, "company_name")

        return self.data

    def generate_quality_report(self):
        if self.data is None:
            raise ValueError(
                f"No data loaded, standardized, and validated for provider: {self.provider}"
            )

        data_quality_metrics = {}

        # Data quality on countries feature
        valid_countries_rate = self.data["country_is_valid"].mean()
        missing_countries_rate = self.data["country_is_missing"].mean()
        invalid_countries_rate = self.data["country_is_invalid"].mean()

        data_quality_metrics["valid_countries_rate"] = valid_countries_rate
        data_quality_metrics["missing_countries_rate"] = missing_countries_rate
        data_quality_metrics["invalid_countries_rate"] = invalid_countries_rate

        # Registration
        missing_registration_rate = self.data["registration_missing"].mean()
        registration_uniqueness = self.data["registration_uniqueness"].mean()

        data_quality_metrics["missing_registration_rate"] = missing_registration_rate
        data_quality_metrics["registration_uniqueness"] = registration_uniqueness

        # Company Names
        missing_company_names = self.data["company_missing"].mean()
        company_name_uniqueness = self.data["company_uniqueness"].mean()

        data_quality_metrics["company_missing"] = missing_company_names
        data_quality_metrics["company_uniqueness"] = company_name_uniqueness

        df = pd.DataFrame(data_quality_metrics, index=[self.provider]).transpose()
        return df
