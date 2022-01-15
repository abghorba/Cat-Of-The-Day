from handlers import CatAPIHandler
import pytest


class TestCatAPIHandler:
    cat_api = CatAPIHandler()

    # Clear the log file.
    with open("log.txt", "w") as f:
        pass

    @pytest.mark.parametrize(
        "category,breed,expected",
        [
            (None, None, "Here is a random cat!"),
            ("sunglass", None, "Here is a cat wearing sunglasses!"),
            ("clothes", None, "Here is a cat wearing clothes!"),
            ("box", None, "Here is a cat in a box!"),
            ("sink", None, "Here is a cat in a sink!"),
            ("space", None, "Here is a cat in space!"),
            ("hat", None, "Here is a cat wearing a hat!"),
            ("tie", None, "Here is a cat wearing a tie!"),
            ("bling", None, "Here is a random cat!"),
            ("stuff", None, "Here is a random cat!"),
            (None, "bengal", "Here is a Bengal cat!"),
            (None, "bambino", "Here is a Bambino cat!"),
            (None, "american shorthair", "Here is a American Shorthair cat!"),
            (None, "javanese", "Here is a Javanese cat!"),
            (None, "egyptian mau", "Here is a Egyptian Mau cat!"),
            (None, "siamese", "Here is a Siamese cat!"),
            ("sunglass", "bengal", "Here is a cat wearing sunglasses!"),
            ("clothes", "bambino", "Here is a cat wearing clothes!"),
            ("box", "american shorthair", "Here is a cat in a box!"),
            ("space", "american shorthair", "Here is a cat in space!"),
            ("bling", "javanese", "Here is a Javanese cat!"),
            ("stuff", "egyptian mau", "Here is a Egyptian Mau cat!"),
            ("thing", "siamese", "Here is a Siamese cat!"),
            ("hat", "kitty kat", "Here is a cat wearing a hat!"),
            ("tie", "pretty kitty", "Here is a cat wearing a tie!"),
            ("clothes", "smelly cat", "Here is a cat wearing clothes!"),                        
        ],
    )
    def test_get_cat_image(self, category, breed, expected):
        cat_image_url, message = self.cat_api.get_cat_image(
            category=category, breed=breed
        )

        print(cat_image_url)
        assert any(image_type in cat_image_url for image_type in ['.jpg', '.png', 'gif'])

        print(message)
        assert expected == message

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
