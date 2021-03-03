############################################
# input

INPUT_DATA=data/segmented
OUTPUT_DATA=cooked/
INPUT_FORMAT=utf8
INPUT_TYPE=segmented
OUTPUT_FORMAT=sl
SENTENCE_LEN_THRESHOLD=1

python3 src/cooker.py \
    --input_data $INPUT_DATA \
    --output_data $OUTPUT_DATA \
    --input_data_format $INPUT_FORMAT \
    --input_data_type $INPUT_TYPE \
    --output_data_format $OUTPUT_FORMAT \
    --sentence_len_threshold $SENTENCE_LEN_THRESHOLD \
    # --exclude_empty_line \
    # --quiet \
