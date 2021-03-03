import argparse
from datetime import datetime
from pathlib import Path
import re
import sys

import constants
import divs
'''
    Script for cooking CTB6 corpus
        - word-level
        - characteristics
'''


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet',
                        '-q',
                        action='store_true',
                        help='Do not report on screen')
    parser.add_argument('--input_data',
                        '-i',
                        type=Path,
                        required=True,
                        help='File path to input data (directory)')
    parser.add_argument('--output_data',
                        '-o',
                        type=Path,
                        default=None,
                        help='File path to output data')
    parser.add_argument(
        '--input_data_format',
        '-f',
        default='utf8',
        help='Choose format of input data among from \'utf8\' (Default: utf8)')
    parser.add_argument(
        '--input_data_type',
        '-t',
        choices=['segmented', 'postagged', 'bracketed'],
        default='segmented',
        help=
        'Choose type of input data among from \'segmented\', \'postagged\', \'brackted\' (Default: segmented)'
    )
    parser.add_argument(
        '--output_data_format',
        default='sl',
        help=
        'Choose format of output data among from \'wl\' and \'sl\' (Default: sl)'
    )
    parser.add_argument(
        '--sentence_len_threshold',
        type=int,
        default=1,
        help=
        'Sentence length threshold. Sentences whose length are lower than the threshold are ignored (Default: 1)'
    )
    parser.add_argument('--exclude_empty_line',
                        action='store_true',
                        help='Specify to exclude empty line')

    args = parser.parse_args()
    return args


class Data(object):
    def __init__(self, train=None, valid=None, test=None):
        self.train = train
        self.valid = valid
        self.test = test


def get_data_paths(path, sort=True):
    return sorted(list(path.glob('*/'))) if sort else list(path.glob('*/'))


def get_trainaing_valididation_and_testing_data_paths(paths):
    train_paths = []
    valid_paths = []
    test_paths = []

    for path in paths:
        if path.suffix == constants.CTB_FILE_SEG_EXT:
            filename = path.stem
            dtype = get_data_division_type(filename)
            if dtype == constants.CTB_TRAIN_DATA:
                train_paths.append(path)
            elif dtype == constants.CTB_VALID_DATA:
                valid_paths.append(path)
            elif dtype == constants.CTB_TEST_DATA:
                test_paths.append(path)

    return train_paths, valid_paths, test_paths


def get_data_division_type(filename):
    fno = int(filename.split(constants.CTB_FILE_PREFIX)[1])
    for indices in divs.CTB_DIVISION['TRAIN']:
        b = indices[0]
        e = indices[1] + 1
        r = range(b, e)
        if fno in r:
            return constants.CTB_TRAIN_DATA

    for indices in divs.CTB_DIVISION['VALID']:
        b = indices[0]
        e = indices[1] + 1
        r = range(b, e)
        if fno in r:
            return constants.CTB_VALID_DATA

    for indices in divs.CTB_DIVISION['TEST']:
        b = indices[0]
        e = indices[1] + 1
        r = range(b, e)
        if fno in r:
            return constants.CTB_TEST_DATA


def load_data(path, data_format, data_type):
    if data_type == 'segmented':
        data = load_segmented_data(path)

    elif data_type == 'postagged':
        data = load_postagged_data(path)

    elif data_type == 'brackted':
        data = load_bracketed_data(path)

    else:
        print('Error: invalid data format: {}'.format(data_format),
              file=sys.stderr)
        sys.exit()

    return data


def load_segmented_data(path):
    dpaths = get_data_paths(path, sort=True)
    train_paths, valid_paths, test_paths = get_trainaing_valididation_and_testing_data_paths(
        dpaths)
    train = []
    valid = []
    test = []

    for train_path in train_paths:
        with open(train_path, 'rt', encoding='utf8') as f:
            for line in f:
                line = line.strip(constants.L_DELIM)
                train.append(line)

    for valid_path in valid_paths:
        with open(valid_path, 'rt', encoding='utf8') as f:
            for line in f:
                line = line.strip(constants.L_DELIM)
                valid.append(line)

    for test_path in test_paths:
        with open(test_path, 'rt', encoding='utf8') as f:
            for line in f:
                line = line.strip(constants.L_DELIM)
                test.append(line)

    return Data(train, valid, test)


def load_postagged_data(path):
    pass


def load_bracketed_data(path):
    pass


def gen_gold_data(data, data_format, threshold=1, exclude_empty_line=False):
    if data_format == constants.SL_FORMAT:
        data = gen_gold_data_SL(data, threshold, exclude_empty_line)

    elif data_format == constants.WL_FORMAT:
        data = gen_gold_data_WL(data, threshold, exclude_empty_line)

    return data


def gen_gold_data_SL(data, threshold=1, exclude_empty_line=False):
    gtrain = []  # gold train data
    gvalid = []  # gold valid data
    gtest = []  # gold test data
    train = data.train  # train lines
    valid = data.valid  # valid lines
    test = data.test  # test lines
    TAG_PATTERN_RE = re.compile(constants.TAG_PATTERN)

    for tr in train:
        if re.match(TAG_PATTERN_RE, tr):  # ignore a line that contains tag
            continue
        tr = tr.strip()
        ws = tr.split(constants.SL_TOKEN_DELIM)  # words sequence
        if len(ws) < threshold or ''.join(
                ws
        ) == constants.CTB_SEG_END_TEXT:  # filter by threshold and ignore ending word
            continue
        if exclude_empty_line and (len(ws) < 2
                                   and len(ws[0]) < 1):  # ignore empty line
            continue
        wl = constants.SL_TOKEN_DELIM.join(ws)
        gtrain.append(wl)

    for va in valid:
        if re.match(TAG_PATTERN_RE, va):
            continue
        va = va.strip()
        ws = va.split(constants.SL_TOKEN_DELIM)
        if len(ws) < threshold or ''.join(
                ws
        ) == constants.CTB_SEG_END_TEXT:  # filter by threshold and ignore ending word
            continue
        if exclude_empty_line and (len(ws) < 2
                                   and len(ws[0]) < 1):  # ignore empty line
            continue
        wl = constants.SL_TOKEN_DELIM.join(ws)
        gvalid.append(wl)

    for te in test:
        if re.match(TAG_PATTERN_RE, te):
            continue
        te = re.sub(TAG_PATTERN_RE, '', te)
        te = te.strip()
        ws = te.split(constants.SL_TOKEN_DELIM)
        if len(ws) < threshold or ''.join(
                ws
        ) == constants.CTB_SEG_END_TEXT:  # filter by threshold and ignore ending word
            continue
        if exclude_empty_line and (len(ws) < 2
                                   and len(ws[0]) < 1):  # ignore empty line
            continue
        wl = constants.SL_TOKEN_DELIM.join(ws)
        gtest.append(wl)

    return Data(gtrain, gvalid, gtest)


def gen_gold_data_WL(data, threshold=1, exclude_empty_line=False):
    gtrain = []  # gold train data
    gvalid = []  # gold valid data
    gtest = []  # gold test data
    train = data.train  # train lines
    valid = data.valid  # valid lines
    test = data.test  # test lines
    TAG_PATTERN_RE = re.compile(constants.TAG_PATTERN)

    for tr in train:
        if re.match(TAG_PATTERN_RE, tr):  # ignore a line that contains tags
            continue
        tr = tr.strip()
        ws = tr.split(constants.SL_TOKEN_DELIM)  # words sequence
        wl = constants.WL_TOKEN_DELIM.join(
            ws
        ) + constants.WL_TOKEN_DELIM  # concat with WL_DELIM for output data
        gtrain.append(wl)

    for va in valid:
        if re.match(TAG_PATTERN_RE, va):
            continue
        va = va.strip()
        ws = va.split(constants.SL_TOKEN_DELIM)
        if len(ws) < threshold or ''.join(
                ws
        ) == constants.CTB_SEG_END_TEXT:  # filter by threshold and ignore ending word
            continue
        if exclude_empty_line and (len(ws) < 2
                                   and len(ws[0]) < 1):  # ignore empty line
            continue
        wl = constants.SL_TOKEN_DELIM.join(ws)
        wl = constants.WL_TOKEN_DELIM.join(ws) + constants.WL_TOKEN_DELIM
        gvalid.append(wl)

    for te in test:
        if re.match(TAG_PATTERN_RE, te):
            continue
        te = te.strip()
        ws = te.split(constants.SL_TOKEN_DELIM)
        if len(ws) < threshold or ''.join(
                ws
        ) == constants.CTB_SEG_END_TEXT:  # filter by threshold and ignore ending word
            continue
        if exclude_empty_line and (len(ws) < 2
                                   and len(ws[0]) < 1):  # ignore empty line
            continue
        wl = constants.WL_TOKEN_DELIM.join(ws) + constants.WL_TOKEN_DELIM
        gtest.append(wl)

    return Data(gtrain, gvalid, gtest)


def log(message, file=sys.stderr):
    print(message, file=file)


def get_data_ext_type(data_type):
    if data_type == constants.DATA_SEG_TYPE:
        return constants.CTB_FILE_SEG
    elif data_type == constants.DATA_POS_TYPE:
        return constants.CTB_FILE_POS
    elif data_type == constants.DATA_SYN_TYPE:
        return constants.CTB_FILE_SYN


def report(data):
    train_sents = data.train
    valid_sents = data.valid
    test_sents = data.test

    n_trsents = len(train_sents)
    n_vasents = len(valid_sents)
    n_tesents = len(test_sents)

    trss = [s.split() for s in train_sents]
    vass = [s.split() for s in valid_sents]
    tess = [s.split() for s in test_sents]

    trss_str = [''.join(s) for s in trss]
    vass_str = [''.join(s) for s in vass]
    tess_str = [''.join(s) for s in tess]

    trws = [w for s in trss for w in s]
    vaws = [w for s in vass for w in s]
    tews = [w for s in tess for w in s]

    n_trwords = len(trws)
    n_vawords = len(vaws)
    n_tewords = len(tews)

    trcs = [c for w in trws for c in w]
    vacs = [c for w in vaws for c in w]
    tecs = [c for w in tews for c in w]

    n_trchars = len(trcs)
    n_vachars = len(vacs)
    n_techars = len(tecs)

    max_trwps = len(max(trss, key=len))
    max_trcps = len(max(trss_str, key=len))
    max_trcpw = len(max(trws, key=len))
    max_vawps = len(max(vass, key=len))
    max_vacps = len(max(vass_str, key=len))
    max_vacpw = len(max(vaws, key=len))
    max_tewps = len(max(tess, key=len))
    max_tecps = len(max(tess_str, key=len))
    max_tecpw = len(max(tews, key=len))

    min_trwps = len(min(trss, key=len))
    min_trcps = len(min(trss_str, key=len))
    min_trcpw = len(min(trws, key=len))
    min_vawps = len(min(vass, key=len))
    min_vacps = len(min(vass_str, key=len))
    min_vacpw = len(min(vaws, key=len))
    min_tewps = len(min(tess, key=len))
    min_tecps = len(min(tess_str, key=len))
    min_tecpw = len(min(tews, key=len))

    avg_trwps = n_trwords / n_trsents  # words/sentence
    avg_trcps = n_trchars / n_trsents  # chars/sentence
    avg_trcpw = n_trchars / n_trwords  # chars/word
    avg_vawps = n_vawords / n_vasents
    avg_vacps = n_vachars / n_vasents
    avg_vacpw = n_vachars / n_vawords
    avg_tewps = n_tewords / n_tesents
    avg_tecps = n_techars / n_tesents
    avg_tecpw = n_techars / n_tewords

    log('### report')
    log('## training data')
    log('# [POST] sent (train): {} ...'.format(n_trsents))
    log('# [POST] word (train): {} ...'.format(n_trwords))
    log('# [POST] char (train): {} ...'.format(n_trchars))
    log('# [POST] words/sent (train): min={} max={} avg={}'.format(
        min_trwps, max_trwps, avg_trwps))
    log('# [POST] chars/sent (train): min={} max={} avg={}'.format(
        min_trcps, max_trcps, avg_trcps))
    log('# [POST] chars/word (train): min={} max={} avg={}'.format(
        min_trcpw, max_trcpw, avg_trcpw))
    log('## validation data')
    log('# [POST] sent (valid): {} ...'.format(n_vasents))
    log('# [POST] word (valid): {} ...'.format(n_vawords))
    log('# [POST] char (valid): {} ...'.format(n_vachars))
    log('# [POST] words/sent (valid): min={} max={} avg={}'.format(
        min_vawps, max_vawps, avg_vawps))
    log('# [POST] chars/sent (valid): min={} max={} avg={}'.format(
        min_vacps, max_vacps, avg_vacps))
    log('# [POST] chars/word (valid): min={} max={} avg={}'.format(
        min_vacpw, max_vacpw, avg_vacpw))
    log('## testing data')
    log('# [POST] sent (test): {} ...'.format(n_tesents))
    log('# [POST] word (test): {} ...'.format(n_tewords))
    log('# [POST] char (test): {} ...'.format(n_techars))
    log('# [POST] words/sent (test): min={} max={} avg={}'.format(
        min_tewps, max_tewps, avg_tewps))
    log('# [POST] chars/sent (test): min={} max={} avg={}'.format(
        min_tecps, max_tecps, avg_tecps))
    log('# [POST] chars/word (test): min={} max={} avg={}'.format(
        min_tecpw, max_tecpw, avg_tecpw))


def cook(args):
    start_time = datetime.now().strftime('%Y%m%d_%H%M')
    if not args.quiet:
        log('Start time: {}\n'.format(start_time))
        log('### arguments')
        for k, v in args.__dict__.items():
            log('# {}={}'.format(k, v))
        log('')

    data_path = args.input_data
    data = load_data(data_path,
                     data_format=args.input_data_format,
                     data_type=args.input_data_type)
    gold_data = gen_gold_data(data,
                              data_format=args.output_data_format,
                              threshold=args.sentence_len_threshold,
                              exclude_empty_line=args.exclude_empty_line)

    if args.output_data:
        data_ext_type = get_data_ext_type(args.input_data_type)
        output_train_data_path = '{}/cooked_ctb6_train_{}.{}.{}'.format(
            args.output_data, start_time, data_ext_type,
            args.output_data_format)
        output_valid_data_path = '{}/cooked_ctb6_valid_{}.{}.{}'.format(
            args.output_data, start_time, data_ext_type,
            args.output_data_format)
        output_test_data_path = '{}/cooked_ctb6_test_{}.{}.{}'.format(
            args.output_data, start_time, data_ext_type,
            args.output_data_format)
        with open(output_train_data_path, 'w', encoding='utf8') as f:
            for train_data in gold_data.train:
                print(train_data, file=f)
            if not args.quiet:
                log('save cooked train data: {}'.format(
                    output_train_data_path))
        with open(output_valid_data_path, 'w', encoding='utf8') as f:
            for valid_data in gold_data.valid:
                print(valid_data, file=f)
            if not args.quiet:
                log('save cooked valid data: {}'.format(
                    output_valid_data_path))
        with open(output_test_data_path, 'w', encoding='utf8') as f:
            for test_data in gold_data.test:
                print(test_data, file=f)
            if not args.quiet:
                log('save cooked test data: {}'.format(output_test_data_path))

    if not args.quiet:
        report(gold_data)


def main():
    args = parse_args()
    cook(args)


if __name__ == '__main__':
    main()
