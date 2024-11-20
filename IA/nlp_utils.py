import spacy
from dateutil.parser import parse

nlp = spacy.load("es_core_news_sm")

def extract_entities_and_dates(question):
    """
    Extrae el nombre del estudiante y las fechas de una pregunta usando spaCy.
    """
    doc = nlp(question)
    student_name = None
    dates = []

    for ent in doc.ents:
        if ent.label_ == "PER":
            student_name = ent.text.strip()
        elif ent.label_ == "DATE":
            try:
                date = parse(ent.text, fuzzy=True)
                dates.append(date)
            except ValueError:
                pass  # Ignorar fechas no válidas

    return student_name, dates
