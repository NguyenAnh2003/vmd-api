from model.vmd_model import VMDModel
from omegaconf import OmegaConf, DictConfig
from libs.libs_func import load_config
from modules.data_pipeline import DataProcessingPipeline
from modules.model_modules import ModelModules
from libs.libs_func import _display_word_mispronounce, _compare_transcript_canonical

# config
conf = load_config("./configs/default.yaml")

# init model modules
model_modules = ModelModules(config=conf)
model = model_modules.get_vmd_model()

# data pipeline
data_pipeline = DataProcessingPipeline()


# service class
def vmd_service(media, text):
    phonetic_emb, canonical_phoneme = data_pipeline.get_feature(
        media, text
    )  # get phonetic embedding and canonical phoneme

    prediction = model.predict(phonetic_emb, canonical_phoneme)

    canonical_phoneme = canonical_phoneme.split()  # split to List

    compared_list = _compare_transcript_canonical(canonical_phoneme, prediction)
    compared_result = _display_word_mispronounce(canonical_phoneme, compared_list)
    text = text.split()  # split target text to align with result

    result = dict(zip(text, compared_result))

    return result