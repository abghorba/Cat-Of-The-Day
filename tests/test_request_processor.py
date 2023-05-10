import pytest

from src.request_processor import RequestProcessor


class TestRequestProcessor:
    @pytest.mark.parametrize(
        "test_request,expected_verb,expected_object",
        [
            ("", "", ""),
            ("Want a savannah", "", ""),
            ("Need me a russian blue", "", ""),
            ("Show me a picture of a siamese cat", "show", "picture siamese cat"),
            ("Send me a picture of a cat wearing sunglasses", "send", "picture cat wearing sunglass"),
            ("Get a cat in a hat", "get", "cat hat"),
            ("I want to see a cat in space!", "see", "cat space"),
            ("Let me see a cat in a box", "see", "cat box"),
            ("I wish to view a cat wearing a tie", "view", "cat wearing tie"),
            ("Show me a domestic shorthair kitty", "show", "domestic shorthair kitty"),
            ("Show me an egyptian mau cat", "show", "egyptian mau cat"),
            ("Can you send me a picture of a javanese kitty?", "send", "picture javanese kitty"),
            ("Will you show me a cat wearing clothes?", "show", "cat wearing clothes"),
            ("I need to view an american shorthair wearing a hat", "view", "american shorthair wearing hat"),
            ("I want to receive a bengal cat", "receive", "bengal cat"),
            ("Give me a norwegian forest cat", "give", "norwegian forest cat"),
        ],
    )
    def test_process_request(self, test_request, expected_verb, expected_object):
        """Tests RequestProcessor.process_request()."""

        request_processor = RequestProcessor()
        verb, object_ = request_processor.process_request(test_request)
        assert verb == expected_verb, f"{verb} != {expected_verb}"
        assert object_ == expected_object, f"{object_} != {expected_object}"

    @pytest.mark.parametrize(
        "keywords,string_,expected",
        [
            ([], "test string", None),
            (["test"], "", None),
            (["key1", "key2"], "i am a key", None),
            (["key 1", "key 2", "key 3"], "I need key1", None),
            (["key1", "key2", "key3"], "I need key1", "key1"),
            (["key1", "key2", "key3"], "I need key1", "key1"),
            (["key1", "key2", "key3"], "I need key1 and key2", "key1"),
            (["key3", "key2", "key1"], "I need key3 and key1", "key3"),
            (["key1", "key2", "key3"], "I need key1", "key1"),
            (["key2", "key1", "key3"], "I need key1 and key2", "key2"),
            (["key1", "key2", "key3", "key4", "key5"], "key4key5key6", "key4"),
        ],
    )
    def test_get_keywords_in_string(self, keywords, string_, expected):
        """Tests RequestProcessor.get_keywords_in_string()."""

        request_processor = RequestProcessor()
        assert request_processor.get_keywords_in_string(keywords, string_) == expected
