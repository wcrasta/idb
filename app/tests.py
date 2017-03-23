import os
import unittest

from app import db
from models import *
class TestCase(unittest.TestCase):

	#Zihao's unit tests
	def test_game_to_review(self):
		game = Game(name = "Zelda", api_id=1) 
		reviews = Reviews(title="Review of Zelda")
		game.reviews.append(reviews)
		self.assertTrue(game.reviews!=None)
		self.assertTrue(reviews.game != None)
	
	def test_platform_to_review(self):
		platform = Platform()
		platform.name = "Test platform"
		reviews = Reviews(title="Test review")
		platform.review.append(reviews)
		self.assertTrue(platform.review!=None)
		self.assertTrue(reviews.platform != None)

	def test_studio_to_game(self):
		studio = Studio()
		game = Game()
		studio.game.append(game)
		self.assertTrue(game.studio==studio)
		self.assertTrue(studio.game!=None)

	def test_platform_to_game(self):
		platform = Platform()
		game = Game()
		platform.games.append(game)
		self.assertTrue(game.platform==platform)
		self.assertTrue(platform.games!=None)


	def test_platform_to_studio(self):
		platform = Platform()
		studio = Studio()
		platform.studio.append(studio)
		self.assertTrue(studio.platform==platform)
		self.assertTrue(platform.studio!=None)


	def test_overriding_relationship(self):
		platform = Platform()
		studio = Studio()
		platform.studio.append(studio)
		self.assertTrue(studio.platform==platform)
		platform2 = Platform()
		platform2.studio.append(studio)
		self.assertTrue(studio.platform==platform2)
		self.assertTrue(platform != platform2)

	def test_unpopulated_is_none(self):
		game = Game()
		self.assertTrue(game.platform_id==None)

	def test_unpopulated_list_is_not_none(self):
		game = Game()
		self.assertTrue(game.reviews!=None)
		self.assertTrue(game.reviews.count()==0)

	def test_list_can_never_be_none(self):
		game = Game()
		with self.assertRaises(TypeError):
			game.reviews = None

	def test_nonkey_attributes_populated(self):
		platform = Platform(generation = 4)
		studio = Studio()
		platform.studio.append(studio)
		self.assertTrue(studio.platform.generation == 4)

	def test_no_relationship(self):
		studio = Studio(name="Riot")
		game = Game(name="LoL")
		self.assertTrue(game.studio_id == None)
		
	def test_foreignkey(self):
		studio = Studio()
		studio.name = "Test Studio"
		game = Game (name = "Test game")
		studio.game.append(game)
		self.assertTrue(game.studio_id == studio.id)

	def test_lazy_dynamic(self):
		platform = Platform()
		platform.name = "Wii"
		game = Game (name = "test game")
		game.genre = "Action"
		platform.games.append(game) 
		self.assertTrue("Select" in platform.games.first())

	def test_link(self):
		reviews = Reviews()
		reviews.title = "Zelda review"
		reviews.url = "zelda.com"
		self.assertFalse("http" in reviews.url)

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
