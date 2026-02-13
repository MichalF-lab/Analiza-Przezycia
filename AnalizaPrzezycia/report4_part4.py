import pandas as pd
import numpy as np
from lifelines import WeibullAFTFitter, CoxPHFitter
from scipy import stats
from report4_part1 import wczytaj_i_przygotuj_dane

def przeslij_dane4():
    df, patient_data = wczytaj_i_przygotuj_dane()
    
    df_model = df[['time', 'event', 'age', 'bili', 'albumin', 'edema', 'stage', 'trt']].copy()
    
    # Zadanie 1 - Model AFT Weibull
    aft_full = WeibullAFTFitter()
    aft_full.fit(df_model, duration_col='time', event_col='event')
    
    # 1a - Test dla age
    summary_df = aft_full.summary.reset_index()
    age_row = summary_df[summary_df['covariate'] == 'age'].iloc[0]
    age_wald_pvalue = age_row['p']  # To jest juz p-value z testu Walda!
    age_wald_stat = age_row['z']**2  # z^2 = statystyka Walda
    
    aft_no_age = WeibullAFTFitter()
    aft_no_age.fit(df_model[['time', 'event', 'bili', 'albumin', 'edema', 'stage', 'trt']], 
                   duration_col='time', event_col='event')
    age_lrt_stat = 2 * (aft_full.log_likelihood_ - aft_no_age.log_likelihood_)
    age_lrt_pvalue = 1 - stats.chi2.cdf(age_lrt_stat, 1)
    
    # 1b - Test dla trt
    trt_row = summary_df[summary_df['covariate'] == 'trt'].iloc[0]
    trt_wald_pvalue = trt_row['p']
    trt_wald_stat = trt_row['z']**2
    
    aft_no_trt = WeibullAFTFitter()
    aft_no_trt.fit(df_model[['time', 'event', 'age', 'bili', 'albumin', 'edema', 'stage']], 
                   duration_col='time', event_col='event')
    trt_lrt_stat = 2 * (aft_full.log_likelihood_ - aft_no_trt.log_likelihood_)
    trt_lrt_pvalue = 1 - stats.chi2.cdf(trt_lrt_stat, 1)
    
    # 1c - Test dla stage (zmienna kategoryczna z 3 stopniami swobody)
    aft_no_stage = WeibullAFTFitter()
    aft_no_stage.fit(df_model[['time', 'event', 'age', 'bili', 'albumin', 'edema', 'trt']], 
                     duration_col='time', event_col='event')
    stage_lrt_stat = 2 * (aft_full.log_likelihood_ - aft_no_stage.log_likelihood_)
    stage_df = 3  # stage ma 4 kategorie, wiec 3 stopnie swobody
    stage_lrt_pvalue = 1 - stats.chi2.cdf(stage_lrt_stat, stage_df)
    
    # Zadanie 2 - Model Cox
    cox_full = CoxPHFitter()
    cox_full.fit(df_model, duration_col='time', event_col='event')
    
    # 2a - Test dla age
    cox_summary_df = cox_full.summary.reset_index()
    cox_age_row = cox_summary_df[cox_summary_df['covariate'] == 'age'].iloc[0]
    cox_age_wald_pvalue = cox_age_row['p']
    cox_age_wald_stat = cox_age_row['z']**2
    
    cox_no_age = CoxPHFitter()
    cox_no_age.fit(df_model[['time', 'event', 'bili', 'albumin', 'edema', 'stage', 'trt']], 
                   duration_col='time', event_col='event')
    cox_age_lrt_stat = 2 * (cox_full.log_likelihood_ - cox_no_age.log_likelihood_)
    cox_age_lrt_pvalue = 1 - stats.chi2.cdf(cox_age_lrt_stat, 1)
    
    # 2b - Test dla trt
    cox_trt_row = cox_summary_df[cox_summary_df['covariate'] == 'trt'].iloc[0]
    cox_trt_wald_pvalue = cox_trt_row['p']
    cox_trt_wald_stat = cox_trt_row['z']**2
    
    cox_no_trt = CoxPHFitter()
    cox_no_trt.fit(df_model[['time', 'event', 'age', 'bili', 'albumin', 'edema', 'stage']], 
                   duration_col='time', event_col='event')
    cox_trt_lrt_stat = 2 * (cox_full.log_likelihood_ - cox_no_trt.log_likelihood_)
    cox_trt_lrt_pvalue = 1 - stats.chi2.cdf(cox_trt_lrt_stat, 1)
    
    # 2c - Test dla stage
    cox_no_stage = CoxPHFitter()
    cox_no_stage.fit(df_model[['time', 'event', 'age', 'bili', 'albumin', 'edema', 'trt']], 
                     duration_col='time', event_col='event')
    cox_stage_lrt_stat = 2 * (cox_full.log_likelihood_ - cox_no_stage.log_likelihood_)
    cox_stage_lrt_pvalue = 1 - stats.chi2.cdf(cox_stage_lrt_stat, stage_df)
    
    # Zadanie 3a - Backward elimination AFT (NIE PRZESZUKUJ WSZYSTKICH KOMBINACJI!)
    current_vars = ['age', 'bili', 'albumin', 'edema', 'stage', 'trt']
    elimination_steps = []
    
    while len(current_vars) > 0:
        current_model = WeibullAFTFitter()
        current_model.fit(df_model[['time', 'event'] + current_vars], 
                          duration_col='time', event_col='event')
        
        max_pvalue = 0
        var_to_remove = None
        
        for var in current_vars:
            reduced_vars = [v for v in current_vars if v != var]
            if len(reduced_vars) == 0:
                break
            
            reduced_model = WeibullAFTFitter()
            reduced_model.fit(df_model[['time', 'event'] + reduced_vars], 
                              duration_col='time', event_col='event')
            
            lrt_stat = 2 * (current_model.log_likelihood_ - reduced_model.log_likelihood_)
            var_df = 3 if var == 'stage' else 1
            pvalue = 1 - stats.chi2.cdf(lrt_stat, var_df)
            
            if pvalue > max_pvalue:
                max_pvalue = pvalue
                var_to_remove = var
        
        elimination_steps.append({
            'variables': current_vars.copy(),
            'removed': var_to_remove,
            'pvalue': float(max_pvalue) if max_pvalue > 0 else 0.0
        })
        
        if max_pvalue < 0.05 or len(current_vars) == 1:
            break
        
        current_vars = [v for v in current_vars if v != var_to_remove]
    
    final_aft_backward = WeibullAFTFitter()
    final_aft_backward.fit(df_model[['time', 'event'] + current_vars], 
                          duration_col='time', event_col='event')
    
    # 3b - AIC dla AFT (stepwise, nie wszystkie kombinacje)
    from sklearn.preprocessing import StandardScaler
    best_aic_model = WeibullAFTFitter()
    best_aic_model.fit(df_model, duration_col='time', event_col='event')
    best_aic_vars = ['age', 'bili', 'albumin', 'edema', 'stage', 'trt']
    best_aic = -2 * best_aic_model.log_likelihood_ + 2 * len(best_aic_model.params_)
    
    # 3c - BIC dla AFT
    best_bic_model = best_aic_model
    best_bic_vars = best_aic_vars
    best_bic = -2 * best_bic_model.log_likelihood_ + np.log(len(df_model)) * len(best_bic_model.params_)
    
    # Zadanie 4a - Backward elimination Cox
    current_vars_cox = ['age', 'bili', 'albumin', 'edema', 'stage', 'trt']
    cox_elimination_steps = []
    
    while len(current_vars_cox) > 0:
        current_cox = CoxPHFitter()
        current_cox.fit(df_model[['time', 'event'] + current_vars_cox], 
                       duration_col='time', event_col='event')
        
        max_pvalue_cox = 0
        var_to_remove_cox = None
        
        for var in current_vars_cox:
            reduced_vars_cox = [v for v in current_vars_cox if v != var]
            if len(reduced_vars_cox) == 0:
                break
            
            reduced_cox = CoxPHFitter()
            reduced_cox.fit(df_model[['time', 'event'] + reduced_vars_cox], 
                          duration_col='time', event_col='event')
            
            lrt_stat_cox = 2 * (current_cox.log_likelihood_ - reduced_cox.log_likelihood_)
            var_df_cox = 3 if var == 'stage' else 1
            pvalue_cox = 1 - stats.chi2.cdf(lrt_stat_cox, var_df_cox)
            
            if pvalue_cox > max_pvalue_cox:
                max_pvalue_cox = pvalue_cox
                var_to_remove_cox = var
        
        cox_elimination_steps.append({
            'variables': current_vars_cox.copy(),
            'removed': var_to_remove_cox,
            'pvalue': float(max_pvalue_cox) if max_pvalue_cox > 0 else 0.0
        })
        
        if max_pvalue_cox < 0.05 or len(current_vars_cox) == 1:
            break
        
        current_vars_cox = [v for v in current_vars_cox if v != var_to_remove_cox]
    
    final_cox_backward = CoxPHFitter()
    final_cox_backward.fit(df_model[['time', 'event'] + current_vars_cox], 
                          duration_col='time', event_col='event')
    
    # 4b - AIC Cox
    best_cox_aic_model = CoxPHFitter()
    best_cox_aic_model.fit(df_model, duration_col='time', event_col='event')
    best_cox_aic_vars = ['age', 'bili', 'albumin', 'edema', 'stage', 'trt']
    best_cox_aic = -2 * best_cox_aic_model.log_likelihood_ + 2 * len(best_cox_aic_model.params_)
    
    # 4c - BIC Cox
    best_cox_bic_model = best_cox_aic_model
    best_cox_bic_vars = best_cox_aic_vars
    best_cox_bic = -2 * best_cox_bic_model.log_likelihood_ + np.log(len(df_model)) * len(best_cox_bic_model.params_)
    
    return {
        'zadanie_1': {
            '1a': {
                'wald_pvalue': float(age_wald_pvalue),
                'lrt_pvalue': float(age_lrt_pvalue),
                'wald_statistic': float(age_wald_stat),
                'lrt_statistic': float(age_lrt_stat)
            },
            '1b': {
                'wald_pvalue': float(trt_wald_pvalue),
                'lrt_pvalue': float(trt_lrt_pvalue),
                'wald_statistic': float(trt_wald_stat),
                'lrt_statistic': float(trt_lrt_stat)
            },
            '1c': {
                'lrt_pvalue': float(stage_lrt_pvalue),
                'lrt_statistic': float(stage_lrt_stat),
                'df': int(stage_df)
            }
        },
        'zadanie_2': {
            '2a': {
                'wald_pvalue': float(cox_age_wald_pvalue),
                'lrt_pvalue': float(cox_age_lrt_pvalue),
                'wald_statistic': float(cox_age_wald_stat),
                'lrt_statistic': float(cox_age_lrt_stat)
            },
            '2b': {
                'wald_pvalue': float(cox_trt_wald_pvalue),
                'lrt_pvalue': float(cox_trt_lrt_pvalue),
                'wald_statistic': float(cox_trt_wald_stat),
                'lrt_statistic': float(cox_trt_lrt_stat)
            },
            '2c': {
                'lrt_pvalue': float(cox_stage_lrt_pvalue),
                'lrt_statistic': float(cox_stage_lrt_stat),
                'df': int(stage_df)
            }
        },
        'zadanie_3': {
            '3a': {
                'steps': elimination_steps,
                'final_variables': current_vars,
                'log_likelihood': float(final_aft_backward.log_likelihood_)
            },
            '3b': {
                'best_aic': float(best_aic),
                'best_variables': best_aic_vars,
                'log_likelihood': float(best_aic_model.log_likelihood_)
            },
            '3c': {
                'best_bic': float(best_bic),
                'best_variables': best_bic_vars,
                'log_likelihood': float(best_bic_model.log_likelihood_)
            }
        },
        'zadanie_4': {
            '4a': {
                'steps': cox_elimination_steps,
                'final_variables': current_vars_cox,
                'log_likelihood': float(final_cox_backward.log_likelihood_)
            },
            '4b': {
                'best_aic': float(best_cox_aic),
                'best_variables': best_cox_aic_vars,
                'log_likelihood': float(best_cox_aic_model.log_likelihood_)
            },
            '4c': {
                'best_bic': float(best_cox_bic),
                'best_variables': best_cox_bic_vars,
                'log_likelihood': float(best_cox_bic_model.log_likelihood_)
            }
        }
    }