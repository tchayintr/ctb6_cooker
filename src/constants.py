'''
    Delimiter symbols
'''

# CTB6.0 delimiters

CTB_FILE_PREFIX = 'chtb_'
CTB_FILE_SEG_EXT = '.seg'
CTB_FILE_POS_EXT = '.pos'
CTB_FILE_SYN_EXT = '.fid'
CTB_FILE_SEG = 'seg'
CTB_FILE_POS = 'pos'
CTB_FILE_SYN = 'fid'
DATA_SEG_TYPE = 'segmented'
DATA_POS_TYPE = 'postagged'
DATA_SYN_TYPE = 'brackted'
W_DELIM = ' '  # word delimiter
POS_DELIM = '_'  # POS delimiter
L_DELIM = '\n'  # line delimiter
CTB_TRAIN_DATA = 'train'
CTB_VALID_DATA = 'valid'
CTB_TEST_DATA = 'test'
# TAG_PATTERN = '<[\w/]+>'
TAG_PATTERN = '<.*?>'
EMPTY_LINE_PATTERN = '^\s*$'

# for data io

DELIMITERS = {'NE_DELIMITER': '\u2582', 'CONTEXT_DELIMITER': '\u2585'}
CTB_SEG_END_TEXT = '（完）'
SL_TOKEN_DELIM = ' '
SL_ATTR_DELIM = '_'
WL_TOKEN_DELIM = '\n'
WL_ATTR_DELIM = '\t'

SL_FORMAT = 'sl'
WL_FORMAT = 'wl'
