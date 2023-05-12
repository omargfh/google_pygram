## Google PyGram

An API interface for Google Book NGrams.

## Installation

```bash
pip install google-pygram
```

## Usage

```python
from google_pygram import GooglePyGram as gpg

pygram = gpg(
    corpus='English',
    corpus_year=2019,
    start_year=1800,
    end_year=2000,
    smoothing=3,
    case_sensitive=False,
    phrases=['hello', 'world']
)

print(pygram.to_df())

#         year         hello     world
# 1800  1800.0  9.921164e-08  0.000379
# 1801  1801.0  6.075895e-08  0.000423
# 1802  1802.0  7.149158e-08  0.000353
# 1803  1803.0  2.593483e-08  0.000338
# 1804  1804.0  8.450996e-08  0.000398
# ...      ...           ...       ...
# 1996  1996.0  1.331358e-06  0.000306
# 1997  1997.0  1.430890e-06  0.000308
# 1998  1998.0  1.523893e-06  0.000317
# 1999  1999.0  1.650712e-06  0.000326
# 2000  2000.0  2.076080e-06  0.000337
```

## Parameters

- `corpus`: The corpus to use. Can be one of the following:
    - `English`
    - `Chinese (simplified)`
    - `French`
    - `German`
    - `Hebrew`
    - `Italian`
    - `Russian`
    - `Spanish`

- `corpus_year`: The year of the corpus to use. Can be one of the following:
    - `2019`
    - `2012`
    - `2009`

- `start_year`: The start year of the ngram. Must be between 1800 and 2000.

- `end_year`: The end year of the ngram. Must be between 1800 and 2000.

- `smoothing`: The smoothing parameter. Must be between 0 and 5.

- `case_sensitive`: Whether or not the ngram is case sensitive. Must be a boolean.

- `phrases`: A list of phrases to search for. Must be a list of strings.

## Methods

- `add_phrase(phrase)`: Adds a phrase to the ngram query.
- `to_df()`: Returns a pandas DataFrame of the ngram.
- `to_csv(filename)`: Saves the ngram to a csv file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
