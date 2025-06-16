import spacy
from nrclex import NRCLex

nlp = spacy.load("en_core_web_sm")

def extract_keywords_and_emotions(prompt):
    doc = nlp(prompt)
    keywords = [token.text for token in doc if token.pos_ in ("NOUN", "VERB", "ADJ")]
    emotion_scores = NRCLex(prompt).top_emotions
    return keywords, emotion_scores
