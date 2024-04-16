import os
import pickle
import requests


class Model:
    """
    모델 기본 클래스 외부 모델을 다운받는 등의 기본 로직이 포함되어있음.
    """

    def __init__(self, version) -> None:
        self.cache_dir = f".cache/{version}"
        if not os.path.isdir(self.cache_dir):
            os.mkdir(self.cache_dir)

    def tokenize(self, string):
        pass

    def padding(self, tokenzied_string):
        pass

    def predict(self, padded_tokenized_string):
        pass

    def download_file(self, url):
        response = requests.get(url)
        file_cache_path = os.path.join(self.cache_dir, os.path.basename(url))
        if os.path.exists(file_cache_path):
            return file_cache_path
        open(file_cache_path, "wb").write(response.content)
        return file_cache_path

    def load_pickle_file(self, path):
        f = open(path, "rb")
        loaded = pickle.load(f)
        f.close()
        return loaded
