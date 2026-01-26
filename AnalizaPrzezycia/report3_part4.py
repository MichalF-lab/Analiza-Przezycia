from report3_part1 import wczyuj_i_przygotuj_dane_lung
from lifelines import WeibullAFTFitter, CoxPHFitter
from scipy import stats

lung_encoded = wczyuj_i_przygotuj_dane_lung()
W = WeibullAFTFitter()
aft = W
aft.fit(lung_encoded, duration_col='time', event_col='status')



try:
    wald_p_age = aft.summary.loc['age', 'p']
except KeyError:
    try:
        wald_p_age = aft.summary.loc[('lambda_', 'age'), 'p']
    except:
        wald_p_age = aft.summary[aft.summary.index.get_level_values(-1) == 'age']['p'].values[0]
print(f"Test Walda: p-value = {wald_p_age:.6f}")



aft_no_age = W
aft_no_age.fit(lung_encoded.drop('age', axis=1), duration_col='time', event_col='status')
ll_full = aft.log_likelihood_
ll_reduced = aft_no_age.log_likelihood_
lrt_stat = -2 * (ll_reduced - ll_full)
df = 1
lrt_p = 1 - stats.chi2.cdf(lrt_stat, df)
print(f"  p-value = {lrt_p:.6f}")



try:
    wald_p_sex = aft.summary.loc['sex', 'p']
except KeyError:
    try:
        wald_p_sex = aft.summary.loc[('lambda_', 'sex'), 'p']
    except:
        wald_p_sex = aft.summary[aft.summary.index.get_level_values(-1) == 'sex']['p'].values[0]
print(f"Test Walda: p-value = {wald_p_sex:.6f}")

aft_no_sex = W
aft_no_sex.fit(lung_encoded.drop('sex', axis=1), duration_col='time', event_col='status')
ll_reduced_sex = aft_no_sex.log_likelihood_
lrt_stat_sex = -2 * (ll_reduced_sex - ll_full)
lrt_p_sex = 1 - stats.chi2.cdf(lrt_stat_sex, df=1)
print(f"  p-value = {lrt_p_sex:.6f}")



if 'ph.ecog' in lung_encoded.columns:
    ecog_cols = ['ph.ecog']
else:
    ecog_cols = [c for c in lung_encoded.columns if 'ph.ecog' in c.lower()]
aft_no_ecog = W
aft_no_ecog.fit(lung_encoded.drop(ecog_cols, axis=1), duration_col='time', event_col='status')

ll_reduced_ecog = aft_no_ecog.log_likelihood_
lrt_stat_ecog = -2 * (ll_reduced_ecog - ll_full)
df_ecog = len(ecog_cols)
lrt_p_ecog = 1 - stats.chi2.cdf(lrt_stat_ecog, df=df_ecog)
print(f"  p-value = {lrt_p_ecog:.6f}")



W = CoxPHFitter()
aft = W
aft.fit(lung_encoded, duration_col='time', event_col='status')



try:
    wald_p_age = aft.summary.loc['age', 'p']
except KeyError:
    try:
        wald_p_age = aft.summary.loc[('lambda_', 'age'), 'p']
    except:
        wald_p_age = aft.summary[aft.summary.index.get_level_values(-1) == 'age']['p'].values[0]
print(f"Test Walda: p-value = {wald_p_age:.6f}")



aft_no_age = W
aft_no_age.fit(lung_encoded.drop('age', axis=1), duration_col='time', event_col='status')
ll_full = aft.log_likelihood_
ll_reduced = aft_no_age.log_likelihood_
lrt_stat = -2 * (ll_reduced - ll_full)
df = 1
lrt_p = 1 - stats.chi2.cdf(lrt_stat, df)
print(f"  p-value = {lrt_p:.6f}")



try:
    wald_p_sex = aft.summary.loc['sex', 'p']
except KeyError:
    try:
        wald_p_sex = aft.summary.loc[('lambda_', 'sex'), 'p']
    except:
        wald_p_sex = aft.summary[aft.summary.index.get_level_values(-1) == 'sex']['p'].values[0]
print(f"Test Walda: p-value = {wald_p_sex:.6f}")

aft_no_sex = W
aft_no_sex.fit(lung_encoded.drop('sex', axis=1), duration_col='time', event_col='status')
ll_reduced_sex = aft_no_sex.log_likelihood_
lrt_stat_sex = -2 * (ll_reduced_sex - ll_full)
lrt_p_sex = 1 - stats.chi2.cdf(lrt_stat_sex, df=1)
print(f"  p-value = {lrt_p_sex:.6f}")



if 'ph.ecog' in lung_encoded.columns:
    ecog_cols = ['ph.ecog']
else:
    ecog_cols = [c for c in lung_encoded.columns if 'ph.ecog' in c.lower()]
aft_no_ecog = W
aft_no_ecog.fit(lung_encoded.drop(ecog_cols, axis=1), duration_col='time', event_col='status')

ll_reduced_ecog = aft_no_ecog.log_likelihood_
lrt_stat_ecog = -2 * (ll_reduced_ecog - ll_full)
df_ecog = len(ecog_cols)
lrt_p_ecog = 1 - stats.chi2.cdf(lrt_stat_ecog, df=df_ecog)
print(f"  p-value = {lrt_p_ecog:.6f}")
