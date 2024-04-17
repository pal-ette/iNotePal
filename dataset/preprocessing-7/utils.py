import re, requests
from hanspell import spell_checker
from pykospacing import Spacing

def get_passport_key():

    """
    네이버에서 '네이버 맞춤법 검사기' 페이지에서 passportKey를 획득
    찾은 값을 spell_checker.py 48 line에 적용한다.
    """

    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"
    res = requests.get(url)

    html_text = res.text

    match = re.search(r'passportKey=([^&"}]+)', html_text)
    if match:
        passport_key = match.group(1)
        return passport_key
    else:
        return False


def fix_spell_checker_py_code(file_path, passportKey):

    """
    획득한 passportkey를 spell_checker.py파일에 적용
    """

    with open(file_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()
        if "passportKey" in content:
            pattern = r"payload = {'passportKey': '.*',"
        else:
            pattern = r"payload = {"

        modified_content = re.sub(pattern, "payload = {"+f"'passportKey': '{passportKey}',", content)

    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)

    return

def fix_passport_key_for_spell_check(file_path):

    key = get_passport_key()
    print("passportKey : ", key)
    fix_spell_checker_py_code(file_path, key)

    return

def get_stopwords(stopwords_file):

    with open(stopwords_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    stopwords = data[0].split(',')

    return stopwords

def handle_missing_values(df, target):

    df = df.dropna(subset=[target]).reset_index(drop=True)
    return df

def konlp_processing(text):

    text = re.sub(r"[^가-힣ㅏ-ㅣㄱ-ㅎA-Za-z0-9,!?\'\`\"]", "", text)
    result = spell_checker.check(text)

    spacing = Spacing()
    if result == 'error':
        text_spacing = spacing(text)
    else:
        text_spacing = spacing(result.checked)

    return text_spacing

def rm_stopwords(text, stopwords):

    text = text.split(" ")
    result = [word for word in text if word not in stopwords]

    return " ".join(result)