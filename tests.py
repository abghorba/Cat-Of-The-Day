from handlers import CatAPIHandler
import pytest


class TestCatAPIHandler():
    cat_api_handler = CatAPIHandler()

    # Clear the log file.
    with open('log.txt', 'w') as f:
        pass

    @pytest.mark.parametrize(
        "category,get_fact,expected", 
        [
            (None, False, "Here is a random kitty!"),
            (None, False, "Here is a random kitty!"),
            ("sunglasses", False, "Here is a kitty with sunglasses!"),
            ("sunglasses", False, "Here is a kitty with sunglasses!"),
            ("clothes", False, "Here is a kitty with clothes!"),
            ("clothes", False, "Here is a kitty with clothes!"),
            ("boxes", False, "Here is a kitty with boxes!"),
            ("boxes", False, "Here is a kitty with boxes!"),
            ("bling", False, "Here is a random kitty!"),
            ("bling", False, "Here is a random kitty!"),
            ("stuff", False, "Here is a random kitty!"),
            ("stuff", False, "Here is a random kitty!"),
            (None, True, "Here is a random kitty!"),
            (None, True, "Here is a random kitty!"),
            (None, True, "Here is a kitty with"),
            (None, True, "Here is a kitty with"),
            ("sunglasses", True, "Here is a kitty with sunglasses!"),
            ("sunglasses", True, "Here is a kitty with sunglasses!"),
            ("clothes", True, "Here is a kitty with clothes!"),
            ("clothes", True, "Here is a kitty with clothes!"),
            ("boxes", True, "Here is a kitty with boxes!"),
            ("boxes", True, "Here is a kitty with boxes!"),
            ("bling", True, "Here is a random kitty!"),
            ("bling", True, "Here is a random kitty!"),
            ("stuff", True, "Here is a random kitty!"),
            ("stuff", True, "Here is a random kitty!"),
        ]
    )
    def test_get_cat_image(self, category, get_fact, expected):
        kitty_image_url, kitty_fact = self.cat_api_handler.get_cat_image(
            category = category,
            get_fact = get_fact
        )

        print(kitty_image_url)
        assert ".jpg" in kitty_image_url or ".png" in kitty_image_url or ".gif" in kitty_image_url

        print(kitty_fact)
        if get_fact:
            assert expected not in kitty_fact
        else:
            assert expected in kitty_fact

