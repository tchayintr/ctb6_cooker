# CTB 6.0 Corpus Cooker
#### _ctb6_cooker_

A tool for extracting segmented words/pos tagged words/trees from CTB 6.0 corpus.

#### Data formats
- **sl**: sentence line
- **wl**: word line
-
#### Functions (tested on utf8 encoding)
- Segmented sentence extraction
- POS tagged sentence extraction (in development)
- Tree extraction (in development)

#### Dataset division based on Yang and Xue, 2012 (https://www.aclweb.org/anthology/P12-1083.pdf)
- train: 81-325, 400-454, 500-554, 590-596, 600-885, 900, 1001-1017, 1019, 1021-1035, 1037-1043, 1045-1059,1062-1071, 1073-1078, 1100-1117, 1130-1131, 1133-1140, 1143-1147, 1149-1151, 2000-2139, 2160-2164, 2181-2279, 2311-2549, 2603-2774, 2820-3079
- dev: 41-80, 1120-1129, 2140-2159, 2280-2294, 2550-2569, 2775-2799, 3080-3109
- test: 
    - newswire: 1-40,901-931
    - magazine: 1018, 1020, 1036, 1044, 1060-1061, 1060-1061, 1072, 1118-1119, 1132, 1141-1142, 1148
    - broadcast news: 2165-2180, 2295-2310, 2570-2602, 2800-2819, 3110-3145

#### Usage
```
usage: ctb6_cooker.py [-h] [--quiet] --input_data INPUT_DATA
                      [--output_data OUTPUT_DATA]
                      [--input_data_format INPUT_DATA_FORMAT]
                      [--input_data_type {segmented,postagged,bracketed}]
                      [--output_data_format OUTPUT_DATA_FORMAT]
                      [--sentence_len_threshold SENTENCE_LEN_THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  --quiet, -q           Do not report on screen
  --input_data INPUT_DATA, -i INPUT_DATA
                        File path to input data (directory)
  --output_data OUTPUT_DATA, -o OUTPUT_DATA
                        File path to output data
  --input_data_format INPUT_DATA_FORMAT, -f INPUT_DATA_FORMAT
                        Choose format of input data among from 'utf8'
                        (Default: utf8)
  --input_data_type {segmented,postagged,bracketed}, -t {segmented,postagged,bracketed}
                        Choose type of input data among from 'segmented',
                        'postagged', 'brackted' (Default: segmented)
  --output_data_format OUTPUT_DATA_FORMAT
                        Choose format of output data among from 'wl' and 'sl'
                        (Default: sl)
  --sentence_len_threshold SENTENCE_LEN_THRESHOLD
                        Sentence length threshold. Sentences whose length are
                        lower than the threshold are ignored (Default: 1)
  ```

  #### Example outputs
  ```
  Start time: 20201110_0016
  
  ### arguments
  # quiet=False
  # input_data=data/segmented
  # output_data=cooked/
  # input_data_format=utf8
  # output_data_format=sl
  # sentence_len_threshold=1
  
  save cooked train data: cooked/cooked_ctb6_train_20201110_0016.sl
  save cooked valid data: cooked/cooked_ctb6_valid_20201110_0016.sl
  save cooked test data: cooked/cooked_ctb6_test_20201110_0016.sl
  ### report
  ## training data
  # [POST] sent (train): 23458 ...
  # [POST] word (train): 641406 ...
  # [POST] char (train): 1056077 ...
  # [POST] words/sent (train): min=1 max=242 avg=27.34274021655725
  # [POST] chars/sent (train): min=1 max=418 avg=45.019907920538834
  # [POST] chars/word (train): min=1 max=21 avg=1.6465031508903878
  ## validation data
  # [POST] sent (valid): 5621 ...
  # [POST] word (valid): 64740 ...
  # [POST] char (valid): 126038 ...
  # [POST] words/sent (valid): min=1 max=145 avg=11.517523572318092
  # [POST] chars/sent (valid): min=2 max=251 avg=22.422700587084147
  # [POST] chars/word (valid): min=1 max=36 avg=1.9468334877973432
  ## testing data
  # [POST] sent (test): 2964 ...
  # [POST] word (test): 81746 ...
  # [POST] char (test): 136385 ...
  # [POST] words/sent (test): min=1 max=189 avg=27.57962213225371
  # [POST] chars/sent (test): min=1 max=278 avg=46.0138326585695
  # [POST] chars/word (test): min=1 max=21 avg=1.6683996770484182
  ```
