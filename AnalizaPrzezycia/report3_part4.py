from report3_part1 import wczyuj_i_przygotuj_dane_lung
from lifelines import WeibullAFTFitter, CoxPHFitter
from scipy import stats
import numpy as np

lung_encoded = wczyuj_i_przygotuj_dane_lung()

aft = WeibullAFTFitter()
aft.fit(lung_encoded, duration_col='time', event_col='status')

# 1A
wald_p_age = aft.summary[aft.summary.index.get_level_values(-1) == 'age']['p'].values[0]
print(f"Test Walda: p-value = {wald_p_age:.6f}")

aft_no_age = WeibullAFTFitter()
aft_no_age.fit(lung_encoded.drop('age', axis=1), duration_col='time', event_col='status')
ll_full = aft.log_likelihood_
ll_reduced = aft_no_age.log_likelihood_
lrt_stat = -2 * (ll_reduced - ll_full)
df = 1
lrt_p = 1 - stats.chi2.cdf(lrt_stat, df)
print(f"  p-value = {lrt_p:.6f}")

# 1B
wald_p_sex = aft.summary[aft.summary.index.get_level_values(-1) == 'sex']['p'].values[0]
print(f"Test Walda: p-value = {wald_p_sex:.6f}")

aft_no_sex = WeibullAFTFitter()
aft_no_sex.fit(lung_encoded.drop('sex', axis=1), duration_col='time', event_col='status')
ll_reduced_sex = aft_no_sex.log_likelihood_
lrt_stat_sex = -2 * (ll_reduced_sex - ll_full)
lrt_p_sex = 1 - stats.chi2.cdf(lrt_stat_sex, df=1)
print(f"  p-value = {lrt_p_sex:.6f}")
ecog_cols = [c for c in lung_encoded.columns if 'ph.ecog' in c.lower()]

# 1C
aft_no_ecog = WeibullAFTFitter()
aft_no_ecog.fit(lung_encoded.drop(ecog_cols, axis=1), duration_col='time', event_col='status')
ll_reduced_ecog = aft_no_ecog.log_likelihood_
lrt_stat_ecog = -2 * (ll_reduced_ecog - ll_full)
df_ecog = len(ecog_cols)
lrt_p_ecog = 1 - stats.chi2.cdf(lrt_stat_ecog, df=df_ecog)
print(f"  p-value = {lrt_p_ecog:.6f}")

# 2
cox = CoxPHFitter()
cox.fit(lung_encoded, duration_col='time', event_col='status')

# 2A
wald_p_age2 = cox.summary.loc['age', 'p']
print(f"Test Walda: p-value = {wald_p_age2:.6f}")

cox_no_age = CoxPHFitter()
cox_no_age.fit(lung_encoded.drop('age', axis=1), duration_col='time', event_col='status')
ll_full = cox.log_likelihood_
ll_reduced = cox_no_age.log_likelihood_
lrt_stat = -2 * (ll_reduced - ll_full)
df = 1
lrt_p2 = 1 - stats.chi2.cdf(lrt_stat, df)
print(f"  p-value = {lrt_p2:.6f}")

# 2B
wald_p_sex2 = cox.summary.loc['sex', 'p']
print(f"Test Walda: p-value = {wald_p_sex2:.6f}")
cox_no_sex = CoxPHFitter()
cox_no_sex.fit(lung_encoded.drop('sex', axis=1), duration_col='time', event_col='status')
ll_reduced_sex = cox_no_sex.log_likelihood_
lrt_stat_sex = -2 * (ll_reduced_sex - ll_full)
lrt_p_sex2 = 1 - stats.chi2.cdf(lrt_stat_sex, df=1)
print(f"  p-value = {lrt_p_sex2:.6f}")

# 2C
ecog_cols = [c for c in lung_encoded.columns if 'ph.ecog' in c.lower()]
cox_no_ecog = CoxPHFitter()
cox_no_ecog.fit(lung_encoded.drop(ecog_cols, axis=1), duration_col='time', event_col='status')
ll_reduced_ecog = cox_no_ecog.log_likelihood_
lrt_stat_ecog = -2 * (ll_reduced_ecog - ll_full)
df_ecog = len(ecog_cols)
lrt_p_ecog2 = 1 - stats.chi2.cdf(lrt_stat_ecog, df=df_ecog)
print(f"  p-value = {lrt_p_ecog2:.6f}")


def przeslij_dane4():
    return {
        "1A": wald_p_age,
        "1A1": lrt_p,
        "1B": wald_p_sex,
        "1B1": lrt_p_sex,
        "1C": lrt_p_ecog,
        "2A": wald_p_age2,
        "2A1": lrt_p2,
        "2B": wald_p_sex2,
        "2B1": lrt_p_sex2,
        "2C": lrt_p_ecog2
    }