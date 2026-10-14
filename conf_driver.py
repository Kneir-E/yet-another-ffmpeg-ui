import json

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    'ffmpeg_dir':'',
    'output_dir':''
}

class Config:
    def __init__(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                self._config = json.load(file)
        except FileNotFoundError:
            self._config = DEFAULT_CONFIG.copy()
            self._save()

    def _save(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self._config, file, indent=4)

    @property
    def ffmpeg_dir(self):
        return self._config["ffmpeg_dir"]

    @ffmpeg_dir.setter
    def ffmpeg_dir(self, value):
        self._config["ffmpeg_dir"] = value
        self._save()

    @property
    def output_dir(self):
        return self._config["output_dir"]

    @output_dir.setter
    def output_dir(self, value):
        self._config["output_dir"] = value
        self._save()


config = Config()