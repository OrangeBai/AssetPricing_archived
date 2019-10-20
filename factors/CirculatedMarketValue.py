import pandas as pd
import config
import os

mv_path = os.path.join(config.extracted_directory, r'CirculateMktValue.csv')
mv = pd.read_csv(mv_path, index_col=0)

month_tags = config.month_split
mv_monthly = {}
for i in range(len(month_tags) - 1):
    mv_monthly[month_tags[i + 1]] = mv[month_tags[i]: month_tags[i + 1]].mean()

# Calculate average market value of month T, save to index 'T+1'
mv_monthly = pd.DataFrame(mv_monthly).T
mv_monthly_path = os.path.join(config.feature_directory, 'M_MktV.csv')
mv_monthly.to_csv(mv_monthly_path)