import os
import pickle
import requests
from app.util.emotion import random_emotion


class InferenceModel:
    """
    모델 기본 클래스 외부 모델을 다운받는 등의 기본 로직이 포함되어있음.
    """

    def __init__(self, version) -> None:
        self.cache_dir = f"{os.getcwd()}/.cache"
        if not os.path.isdir(self.cache_dir):
            os.mkdir(self.cache_dir)
        self.cache_version_dir = f"{self.cache_dir}/{version}"
        if not os.path.isdir(self.cache_version_dir):
            os.mkdir(self.cache_version_dir)

    def tokenize(self, string):
        pass

    def padding(self, tokenzied_string):
        pass

    def predict(self, padded_tokenized_string):
        return random_emotion()

    def download_file(self, url):
        response = requests.get(url)
        file_cache_path = os.path.join(self.cache_version_dir, os.path.basename(url))
        if os.path.exists(file_cache_path):
            return file_cache_path
        open(file_cache_path, "wb").write(response.content)
        return file_cache_path

    def load_pickle_file(self, path):
        f = open(path, "rb")
        loaded = pickle.load(f)
        f.close()
        return loaded
