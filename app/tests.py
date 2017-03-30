# pylint: disable = import-error
# pylint: disable = missing-docstring
import unittest


from models import Game, Studio, Platform, Reviews


class TestCase(unittest.TestCase):

    # Zihao's unit tests

    # Tests that reviews are being properly stored in games

    def test_game_to_review(self):
        game = Game(name="Zelda", api_id=1)
        reviews = Reviews(title="Review of Zelda")
        game.reviews.append(reviews)
        self.assertTrue(game.reviews == None)
        self.assertTrue(reviews.game != None)

    # Tests that platform reviews are being stored in platforms
    def test_platform_to_review(self):
        platform = Platform()
        platform.name = "Test platform"
        reviews = Reviews(title="Test review")
        platform.review.append(reviews)
        self.assertTrue(platform.review != None)
        self.assertTrue(reviews.platform != None)

    # Tests that game can be stored in studio and that the relation
    # Automatically stores the studio in game
    def test_studio_to_game(self):
        studio = Studio()
        game = Game()
        studio.game.append(game)
        self.assertTrue(game.studio == studio)
        self.assertTrue(studio.game != None)

    # Tests that game can be stored in platform and that the relation
    # Automatically stores the platform in game
    def test_platform_to_game(self):
        platform = Platform()
        game = Game()
        platform.games.append(game)
        self.assertTrue(game.platform == platform)
        self.assertTrue(platform.games != None)

    # Tests that studio can be stored in platform and that the relation
    # Automatically stores the platform in studio
    def test_platform_to_studio(self):
        platform = Platform()
        studio = Studio()
        platform.studio.append(studio)
        self.assertTrue(studio.platform == platform)
        self.assertTrue(platform.studio is not None)

    # Tests to see that relationships will properly override when
    # a variable is changed
    def test_overriding_relationship(self):
        platform = Platform()
        studio = Studio()
        platform.studio.append(studio)
        self.assertTrue(studio.platform == platform)
        platform2 = Platform()
        platform2.studio.append(studio)
        self.assertTrue(studio.platform == platform2)
        self.assertTrue(platform != platform2)

    # Checks default values are set to none
    def test_unpopulated_is_none(self):
        game = Game()
        self.assertTrue(game.platform_id is None)

    # Makes sure that the lists are initalized to empty lists
    def test_unpopulated_list_not_none(self):
        game = Game()
        self.assertTrue(game.reviews is not None)
        self.assertTrue(game.reviews.count() == 0)

    # Makes sure that it is not possible to make a list
    # attribute none
    def test_list_can_never_be_none(self):
        game = Game()
        with self.assertRaises(TypeError):
            game.reviews = None

    # Tests that keys can be set by name
    def test_noattributes_populated(self):
        platform = Platform(generation=4)
        studio = Studio()
        platform.studio.append(studio)
        self.assertTrue(studio.platform.generation == 4)

    # Tests that no relationship exist before establishing
    def test_no_relationship(self):
        game = Game(name="LoL")
        self.assertTrue(game.studio_id is None)

    # Tests that the relationship automatically set up the foreign keys
    def test_foreignkey(self):
        studio = Studio()
        studio.name = "Test Studio"
        game = Game(name="Test game")
        studio.game.append(game)
        self.assertTrue(game.studio_id == studio.id)

    # Tests that the classes are loading dynamically
    def test_lazy_dynamic(self):
        platform = Platform()
        platform.name = "Wii"
        game = Game(name="test game")
        game.genre = "Action"
        platform.games.append(game)
        self.assertTrue("SELECT" in str(platform.games))

    # Makes sure that the websites do not start with http
    def test_link(self):
        reviews = Reviews()
        reviews.title = "Zelda review"
        reviews.url = "zelda.com"
        self.assertFalse("http" in reviews.url)

    # Tests that multiple relations are set up as attributes are being set
    def test_multiple_relationships(self):
        platform = Platform(name="test")
        game = Game(name="Zelda")
        review = Reviews(title="review of zelda")
        platform.games.append(game)
        platform.review.append(review)
        self.assertTrue(platform.games.first().id != 0)
        self.assertTrue(platform.review.first().title == "review of zelda")
        self.assertTrue(game.platform_id == platform.id)
        self.assertTrue(review.platform_id == platform.id)

if __name__ == '__main__':
    unittest.main()
    