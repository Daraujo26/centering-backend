from nltk.tokenize.punkt import PunktSentenceTokenizer
from allennlp.predictors.predictor import Predictor
import allennlp_models.coref

tokenizer = PunktSentenceTokenizer()
predictor = Predictor.from_path(
    "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz",
    predictor_name="coreference_resolution"
)

# Group sentences into logical utterances
def group_sentences(sentences):
    grouped = []
    current_group = []

    for sentence in sentences:
        current_group.append(sentence)
        if sentence.strip()[-1] in {'.', '!', '?', ';', ':'}:  # End of an utterance
            grouped.append(" ".join(current_group))
            current_group = []

    if current_group:  # Handle any leftover sentences
        grouped.append(" ".join(current_group))

    return grouped

def process_text(text):
    sentences = tokenizer.tokenize(text)
    grouped_sentences = group_sentences(sentences)  # Group sentences into logical utterances
    coref_result = predictor.predict(document=text)
    return grouped_sentences, coref_result['clusters'], coref_result['document']
