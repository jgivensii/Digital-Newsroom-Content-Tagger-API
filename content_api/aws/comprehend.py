from content_api.aws_config import get_client
import os


COMPREHEND_MIN_CONFIDENCE = float(os.environ.get("COMPREHEND_MIN_CONFIDENCE", 85))

def get_text_key_phrases(Text_Input: str, Native_language = 'en') -> dict:
    """ Calls AWS Comprehend detect_key_phrases to extract a dict of key phrases embedded within a text"""
    response = get_client("comprehend").detect_key_phrases(Text= Text_Input, LanguageCode= Native_language)
    key_phrases = [{'Key_Phrase': phrase['Text'], 'Confidence': phrase['Score']} for phrase in response['KeyPhrases']] 
    
    return key_phrases    

def dedupe_phrases(key_phrases: list[dict]) -> list[dict]:
    normalized = [
        {   "Key_Phrase": key["Key_Phrase"].strip().lower(),
            "Confidence": key["Confidence"],
            "_original": key
        }
        for key in key_phrases
    ]

    seen = set()
    unique = []
    for item in normalized:
        key = (item["Key_Phrase"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Remove substrings (keep longest)
    final = []
    for item in unique:
        text = item["Key_Phrase"]
        if not any(
            text != other["Key_Phrase"] and text in other["Key_Phrase"]
            for other in unique
        ):
            final.append(item["_original"])

    return final

def get_text_entities(Text_Input:str, Native_Language = 'en') -> dict:
    """ Calls AWS Comprehend detect_entities to extract a dict of entities embedded within a text"""
    response = get_client("comprehend").detect_entities(Text=Text_Input, LanguageCode = Native_Language)
    entities = [{'Entity': entity['Type'], 'Entity_Text': entity['Text'], 'Confidence': entity['Score']} for entity in response['Entities']]
    
    return entities 

def dedupe_entities(entities: list[dict]) -> list[dict]:
    normalized = [
        {   "Entity": ent["Entity"],
            "Entity_Text": ent["Entity_Text"].strip().lower(),
            "Confidence": ent["Confidence"],
            "_original": ent
        }
        for ent in entities
    ]

    seen = set()
    unique = []
    for item in normalized:
        key = (item["Entity_Text"], item["Entity"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Remove substrings (keep longest)
    final = []
    for item in unique:
        text = item["Entity_Text"]
        if not any(
            text != other["Entity_Text"] and text in other["Entity_Text"]
            for other in unique
        ):
            final.append(item["_original"])

    return final