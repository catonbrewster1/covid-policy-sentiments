from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification


def get_model(model):
    """Loads model from Hugginface model hub"""
    try:
        model = AutoModelForSequenceClassification.from_pretrained(model)
        model.save_pretrained("./model")
    except Exception as e:
        raise (e)


def get_tokenizer(tokenizer):
    """Loads tokenizer from Hugginface model hub"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        tokenizer.save_pretrained("./model")
    except Exception as e:
        raise (e)

def get_config(configuration):
    """ Loads tokenizer from Hugginface model hug"""
    try:
        config = AutoConfig.from_pretrained(model_path)
        config.save_pretrained("./model")
    except Exception as e:
        raise (e)

get_model("daveni/twitter-xlm-roberta-emotion-es")
get_config("daveni/twitter-xlm-roberta-emotion-es")
get_tokenizer("daveni/twitter-xlm-roberta-emotion-es")
