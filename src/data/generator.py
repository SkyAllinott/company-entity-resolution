import numpy as np

import config as cfg
from data_provider import DataProvider

generator = np.random.default_rng(seed = 4)


"""
Generate the true data
"""
source_of_truth = DataProvider("Envirotech", quality_rules={})
actual_companies = source_of_truth.generate_reference_data(generator=generator, records=1000)

"""
Generate the providers data, which is a subset of the true data with synthetic quality
issues like missingness, invalid entries, etc. 
"""
providers = ["Envirotech", "FinData", "BigData"]
for provider in providers:
    provider_data = DataProvider(provider, quality_rules=cfg.provider_quality)
    provider_data.generate_provider_data(companies=actual_companies, generator=generator)