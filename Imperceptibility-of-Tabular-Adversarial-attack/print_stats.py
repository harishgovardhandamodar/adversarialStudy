import pandas as pd
imp_df = pd.read_csv('all_imp.csv')
sr_df = pd.read_csv('success_rate.csv')

print('=== Dataset Stats ===')
for d in ['adult','breast_cancer','compas','diabetes','german']:
    s = imp_df[imp_df['dataset']==d]
    print(f'{d}: {len(s)} evals, {s.attack_success.mean()*100:.1f}% success')

print()
print('=== Model Stats ===')
for m in ['LR','MLP','SVC']:
    s = imp_df[imp_df['model']==m]
    print(f'{m}: {len(s)} evals, {s.attack_success.mean()*100:.1f}% success')

print()
print('=== Attack x Model x Dataset Success Rates ===')
# Detailed breakdown
for m in ['LR','MLP','SVC']:
    print(f'\n--- {m} ---')
    for att in ['deepfool','carlini_l_2','fgsm_l_inf']:
        print(f'\n  {att}:')
        for d in ['adult','german','compas','diabetes','breast_cancer']:
            s = imp_df[(imp_df['model']==m) & (imp_df['attack']==att) & (imp_df['dataset']==d)]
            if len(s) > 0:
                print(f'    {d}: {s.attack_success.mean()*100:.1f}% (n={len(s)})')

print('\n=== L2 Stats ===')
for att in ['deepfool','carlini_l_2','fgsm_l_inf']:
    s = imp_df[(imp_df['attack']==att) & (imp_df['attack_success']==1)]
    if len(s) > 0:
        print(f'{att}: median_L2={s.eval_L2.median():.6f}, mean_L2={s.eval_L2.mean():.6f}, min_L2={s.eval_L2.min():.6f}')

print('\n=== Sensitivity Stats ===')
for att in ['deepfool','carlini_l_2','fgsm_l_inf']:
    s = imp_df[(imp_df['attack']==att) & (imp_df['attack_success']==1)]
    if len(s) > 0:
        print(f'{att}: median_Sen={s.eval_Sen.median():.6f}, mean_Sen={s.eval_Sen.mean():.6f}')

print('\n=== Mahalanobis Stats ===')
for att in ['deepfool','carlini_l_2','fgsm_l_inf']:
    s = imp_df[(imp_df['attack']==att) & (imp_df['attack_success']==1)]
    if len(s) > 0:
        print(f'{att}: median_Maha={s.eval_Mahalanobis.median():.6f}, mean_Maha={s.eval_Mahalanobis.mean():.6f}')
