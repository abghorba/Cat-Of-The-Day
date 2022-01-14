from handlers import CatAPIHandler
import pytest


class TestCatAPIHandler:
    cat_api = CatAPIHandler()

    # Clear the log file.
    with open("log.txt", "w") as f:
        pass

    @pytest.mark.parametrize(
        "category,get_fact,expected",
        [
            (None, False, "Here is a random cat!"),
            (None, False, "Here is a random cat!"),
            ("sunglass", False, "Here is a cat wearing sunglasses!"),
            ("sunglass", False, "Here is a cat wearing sunglasses!"),
            ("clothes", False, "Here is a cat wearing clothes!"),
            ("clothes", False, "Here is a cat wearing clothes!"),
            ("box", False, "Here is a cat in a box!"),
            ("box", False, "Here is a cat in a box!"),
            ("bling", False, "Here is a random cat!"),
            ("bling", False, "Here is a random cat!"),
            ("stuff", False, "Here is a random cat!"),
            ("stuff", False, "Here is a random cat!"),
            (None, True, "Here is a random cat!"),
            (None, True, "Here is a random cat!"),
            ("sunglass", True, "Here is a cat wearing sunglasses!"),
            ("sunglass", True, "Here is a cat wearing sunglasses!"),
            ("clothes", True, "Here is a cat wearing clothes!"),
            ("clothes", True, "Here is a cat wearing clothes!"),
            ("box", True, "Here is a cat in a box!"),
            ("box", True, "Here is a cat in a box!"),
            ("bling", True, "Here is a random cat!"),
            ("bling", True, "Here is a random cat!"),
            ("stuff", True, "Here is a random cat!"),
            ("stuff", True, "Here is a random cat!"),
        ],
    )
    def test_get_cat_image(self, category, get_fact, expected):
        kitty_image_url, kitty_fact = self.cat_api.get_cat_image(
            category=category, get_fact=get_fact
        )

        print(kitty_image_url)
        assert (
            ".jpg" in kitty_image_url
            or ".png" in kitty_image_url
            or ".gif" in kitty_image_url
        )

        print(kitty_fact)
        if get_fact:
            assert expected not in kitty_fact
        else:
            assert expected in kitty_fact

    @pytest.mark.parametrize(
        "expected_key,expected_id",
        [
            ("box", 5),
            ("sunglass", 4),
            ("hat", 1),
            ("clothes", 15),
            ("sink", 14),
            ("space", 2),
            ("tie", 7),
        ],
    )
    def test_get_category_ids(self, expected_key, expected_id):
        # No need to call the get_category_ids function as it is
        # called upon instantiating the CatAPIHandler object
        assert self.cat_api.CATEGORY_IDS[expected_key] == expected_id

    @pytest.mark.parametrize(
        "expected_key,expected_id",
        [
            ("abyssinian", "abys"),
            ("aegean", "aege"),
            ("american bobtail", "abob"),
            ("american curl", "acur"),
            ("american shorthair", "asho"),
            ("american wirehair", "awir"),
            ("arabian mau", "amau"),
            ("australian mist", "amis"),
            ("balinese", "bali"),
            ("bambino", "bamb"),
            ("bengal", "beng"),
            ("birman", "birm"),
            ("bombay", "bomb"),
            ("british longhair", "bslo"),
            ("british shorthair", "bsho"),
            ("burmese", "bure"),
            ("burmilla", "buri"),
            ("california spangled", "cspa"),
            ("chantilly-tiffany", "ctif"),
            ("chartreux", "char"),
            ("chausie", "chau"),
            ("cheetoh", "chee"),
            ("colorpoint shorthair", "csho"),
            ("cornish rex", "crex"),
            ("cymric", "cymr"),
            ("cyprus", "cypr"),
            ("devon rex", "drex"),
            ("donskoy", "dons"),
            ("dragon li", "lihu"),
            ("egyptian mau", "emau"),
            ("european burmese", "ebur"),
            ("exotic shorthair", "esho"),
            ("havana brown", "hbro"),
            ("himalayan", "hima"),
            ("japanese bobtail", "jbob"),
            ("javanese", "java"),
            ("khao manee", "khao"),
            ("korat", "kora"),
            ("kurilian", "kuri"),
            ("laperm", "lape"),
            ("maine coon", "mcoo"),
            ("malayan", "mala"),
            ("manx", "manx"),
            ("munchkin", "munc"),
            ("nebelung", "nebe"),
            ("norwegian forest cat", "norw"),
            ("ocicat", "ocic"),
            ("oriental", "orie"),
            ("persian", "pers"),
            ("pixie-bob", "pixi"),
            ("ragamuffin", "raga"),
            ("ragdoll", "ragd"),
            ("russian blue", "rblu"),
            ("savannah", "sava"),
            ("scottish fold", "sfol"),
            ("selkirk rex", "srex"),
            ("siamese", "siam"),
            ("siberian", "sibe"),
            ("singapura", "sing"),
            ("snowshoe", "snow"),
            ("somali", "soma"),
            ("sphynx", "sphy"),
            ("tonkinese", "tonk"),
            ("toyger", "toyg"),
            ("turkish angora", "tang"),
            ("turkish van", "tvan"),
            ("york chocolate", "ycho"),
        ],
    )
    def test_get_breed_ids(self, expected_key, expected_id):
        # No need to call the get_breed_ids function as it is
        # called upon instantiating the CatAPIHandler object
        assert self.cat_api.BREED_IDS[expected_key] == expected_id
