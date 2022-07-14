import pytest

from helpers.query_processor import QueryProcessor
from nltk.corpus import stopwords


STOP_WORDS = set(stopwords.words('english'))

query_processor = QueryProcessor()


@pytest.mark.parametrize(
    "text,expected_cleaned_text",
    [
        ("What a marvelous day it is today!", "what a marvelous day it is today"),
        ("There isn't a place I'd rather be.", "there isn't a place i'd rather be"),
        (" why That There is SIMPLY MAGNIFICENT, I must say... ", "why that there is simply magnificent i must say"),
        ("", ""),
        (" ", ""),
        ("!@#$%^&*()-+=][;\".,`~}{", ""),
        (None, "")
    ]
)
def test_clean_test(text, expected_cleaned_text):
    """
    Tests that clean_text() works as intended:
    
    'Strips leading/trailing whitespace, strips punctuation, 
    and converts string to lowercase.' 
    
    :param text: str 
    :param expected_clean_text: str 
    """
    
    cleaned_text = query_processor._clean_text(text)
    assert cleaned_text == expected_cleaned_text


@pytest.mark.parametrize(
    "text,expected_preprocessed_text",
    [
        ("", []),
        ("", []),
        ("", []),
        ("", []),
        ("", []),
    ]
)
def test_preprocess_text(text, expected_preprocessed_text):
    """
    Test that preprocess_text() works as intended:

    'Preprocesses text by stripping whitespace, removing
    punctuation, changing all characters to lowercase,
    tokenizing by whitespaces, and lemmatizing each word.'

    :param text: str
    :param expected_preprocessed_text: list
    """

    preprossed_text = query_processor._preprocess_text(text)
    assert preprossed_text == expected_preprocessed_text


@pytest.mark.parametrize(
    "keywords,text,expected_keywords_found",
    [
        (
            {"crystal", "blue", "persuasion"},
            "Crystal blue Persuasion, hmm, hmm It's a new vibration CrYsTal blue persuasion Crystal Blue persuasion",
            {"crystal": 3, "blue": 3, "persuasion": 3}
        ),
        (
            {"lorem", "magna", "nonsense"},
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            {"lorem": 1, "magna": 1}
        ),
        (
            {"man", "silver", "heaven"},
            "There's a lady who's sure all that glitters is gold. And she's buying a stairway to heaven.",
            {"heaven": 1}
        ),
        (
            {"taking", "everything"},
            "Takin' everythin' in my stride",
            {}
        ),
        (
            STOP_WORDS,
            " ".join(stopwords.words('english')),
            {}
        )
    ]
)
def test_find_keywords_in_text(keywords, text, expected_keywords_found):
    """
    Tests that find_keywords_in_text() works as intended:

    'Given a set of keywords, returns a dictionary with
    the found keywords and the frequency of the keyword in
    text.'

    :param keywords:
    :param text:
    :param expected_keywords_found:
    """
    
    keywords_found = query_processor.find_keywords_in_text(keywords, text)
    assert keywords_found == expected_keywords_found


@pytest.mark.parametrize(
    "key_phrases,text,expected_key_phrases_found",
    [
        (
            {"crystal blue persuasion"},
            "Crystal blue Persuasion, hmm, hmm It's a new vibration CrYsTal blue persuasion Crystal Blue persuasion",
            {"crystal blue persuasion": 3}
        ),
        (
            {"lorem ipsum dolor", "magna aliqua", "nonsensical text"},
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            {"lorem ipsum dolor": 1, "magna aliqua": 1}
        ),
        (
            {"man silver", "heaven"},
            "There's a lady who's sure all that glitters is gold. And she's buying a stairway to heaven.",
            {"heaven": 1}
        ),
        (
            {"taking everything"},
            "Takin' everythin' in my stride",
            {}
        ),
        (
            STOP_WORDS,
            " ".join(stopwords.words('english')),
            {}
        )
    ]
)
def test_find_key_phrases_in_text(key_phrases, text, expected_key_phrases_found):
    """
    Tests that find_key_phrases_in_text() works as intended:

    'Given a set of key phrases, returns a dictionary with
    the found key phrases and the frequency of the keyphrases in
    text.'

    :param key_phrases:
    :param text:
    :param expected_key_phrases_found:
    """
    
    key_phrases_found = query_processor.find_key_phrases_in_text(key_phrases, text)
    assert key_phrases_found == expected_key_phrases_found
    