'''
Run the script with:
```
python run_tsfresh.py path_to_your_csv.csv

- Your csv must be space delimited.
- Output is saved as path_to_your_csv.features.csv

```
e.g.:
```
python run_tsfresh.py data.txt
```

A corresponding csv containing time series features will be 
saved as path_to_your_csv.features.csv
'''

import sys
import numpy as np
import pandas as pd
from tsfresh import extract_features, extract_relevant_features, select_features


def _preprocess(df):
	'''
	given a dataframe where records are stored row-wise, rearrange it 
	such that records are stored column-wise.
	'''
	
	# transpose since tsfresh reads times series data column-wise, not row-wise
	df_t = df.transpose()
	
	master_df = pd.DataFrame(df_t[0])
	master_df['id'] = 0

	for i in range(len(df.columns)):
	    temp_df = pd.DataFrame(df_t.iloc[i])
	    temp_df['id'] = i
	    master_df = pd.DataFrame(np.vstack([master_df, temp_df]))
	return master_df


if __name__ == '__main__':

	# read csv, transpose, extract features
	fname_in = sys.argv[1]
	df = pd.read_csv(fname_in, delim_whitespace=True, header=None)
	df_rearranged = _preprocess(df)
	df_features = extract_features(df_rearranged, column_id=1)

	# re-cast index from float to int
	df_features.index = df_features.index.astype('int')

	# write to disk
	fname_out = fname_in + '.features.csv' 
	df_features.to_csv(fname_out)
