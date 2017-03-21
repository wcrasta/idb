import os
import unittest

from app import app, db
from models import *
class TestCase(unittest.TestCase):

	#Zihao's unit tests
	def test_game_to_review(self):
		game = Game(name = "Zelda", api_id=1) 
		reviews = Reviews(title="Review of Zelda")
		game.reviews.add(reviews)
		self.assertTrue(game.reviews!=None)
		self.aseertTrue(reviews.game_id != None)
	
	def test_platform_to_review(self):
		platform = Platform()
		platform.name = "Test platform"
		reviews = Reviews(title="Test review")
		platform.review.add(review)
		self.assertTrue(plateform.review!=None)
		self.assertTrue(reviews.platform_id != None)

	def test_no_relationship(self):
		studio = Studio(name="Riot")
		game = Game(name="LoL")
		self.assertTrue(game.studio_id == None)
		
	


if __name__ == '__main__':
    unittest.main()
