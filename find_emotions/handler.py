from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification
import numpy as np
import json
from scipy.special import softmax
import traceback


def find_emotions(text, max=False):
    '''
    Function that takes a text and identifies the predominance of each of the
    7 categories of emotions (anger, disgust, sadness, fear, surprise, joy,
    others) based on this HuggingFace model:
    https://huggingface.co/daveni/twitter-xlm-roberta-emotion-es?text=hola
    Input:
        text (str) text to be analyzed
        max (bol) boolean indicating if only returns dominant emotion,
                  or all emotions prevalences
    Output:
        ranking (str) contains the emotions and percentage of prevalence
                      in text
    '''

    tokenizer = AutoTokenizer.from_pretrained("./model")
    model = AutoModelForSequenceClassification.from_pretrained("./model")
    config = AutoConfig.from_pretrained("./model")

    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    rv_ranking = ''
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        if max:
            rv_ranking += f"{l} {np.round(float(s), 4)} "
            break
        else:
            rv_ranking += f"{i+1}) {l} {np.round(float(s), 4)} "
    return rv_ranking


def handler(event, context):
    try:
        if 'source' in event and event["source"] == 'serverless-plugin-warmup':
            # lambda warm-up
            return {
                "statusCode": 200,
                "body": "OK",
            }
        body = json.loads(event['body'])
        text = body['text']
        max = body['max']
        results = find_emotions(text, max)
        return {
            "statusCode": 200,
            "body": json.dumps({"results": results})
        }
    except Exception:
        trace = str(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps({"error": trace}),
        }
