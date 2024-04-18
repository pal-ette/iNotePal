from utils import *
import time, os, pickle
import pandas as pd

if __name__=='__main__':

    data = 'conv-7_dataset.csv'
    df = pd.read_csv(data)
    # print(df.head())
    # preprocessed_file_name = 'preprocessed.csv'

    if not os.path.exists('output'):
        os.makedirs('output')

    # to run hanspell
    # set file_path to dir of spell_checker.py
    file_path = 'C:/Users/Harmony01/Desktop/test/.venv/Lib/site-packages/hanspell/spell_checker.py'
    fix_passport_key_for_spell_check(file_path)

    stopwords_file = 'stop_words.txt'

    start = time.time()
    stopwords = get_stopwords(stopwords_file)

    preprocessed = []
    # set start row
    # due to loss of connection (not always happened, just in case)
    num_start = 83796
    for row in df[num_start:].itertuples():
        print(row.Index, row.sentence)

        preprocessed_sentence = spell_check(row.sentence)
        # preprocessed_sentence = new_spacing(preprocessed_sentence)
        # preprocessed_sentence = rm_stopwords(preprocessed_sentence, stopwords)
        preprocessed.append(preprocessed_sentence)

        with open(f"output/preprocessed_{num_start}_contain_stopwords.pkl", 'wb') as f:
            pickle.dump(preprocessed, f)

    end = time.time()

    print(f'Spell and spacing check from {len(df)} rows take {end - start} sec')

    # df['preprocessed'] = preprocessed
    # df.to_csv(preprocessed_file_name, index=False, header=True)