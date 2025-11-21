from django.test import TestCase
from .models import Player, Tile
from .views import treasures, create_board,pick
from django.test import RequestFactory
from django.db.models import Q

# Create your tests here.

class BoardGameTestCase(TestCase):
    def test_create_two_player(self):
        self.client.post('/game/create/')
        player1 = Player.objects.get(name="One", score=0)
        player2 = Player.objects.get(name="Two", score=0)
        self.assertEqual(player1.name, "One")
        self.assertEqual(player2.name,"Two")
        self.assertEqual(player1.score, 0)
        self.assertEqual(player2.score, 0)

    def test_create_hundred_board_tiles(self):
       
        self.client.post('/game/create/')
        tile = Tile.objects.all().count()
        self.assertEqual(tile,100)
   
    def test_treasures_created(self):
        
        self.client.post('/game/create/')

        print(Tile.objects.filter(~Q(value="_")))
        treasures = 0
        for i in range(10):
            for j in range(10):
                tile = Tile.objects.get(row=i, col=j)
                if tile.value == "_":
                    tile_value = 0
                    
                else:
                    tile_value = int(tile.value)     
                    treasures += tile_value

        self.assertEqual(treasures, 30)
        print(treasures)
        
 
 #this one checks updated score , redirect and no treasure found
    def test_updated_score(self):
        self.client.post('/game/create/')

        score = 0

        for i in range(10):
            for j in range(10):
                tile = Tile.objects.get(row=i, col=j)
                response = self.client.post(f'/game/pick/One/{i}/{j}/')
                
                player = Player.objects.get(name="One")

                if tile.value == "_":
                   tile_value = 0
                   self.assertIn('No treasure found', response.content.decode())

                else:
                    #check redirect as well
                    self.assertEqual(response.url, '/game/')
                    tile_value = int(tile.value)
                    score += tile_value
                    print("score" ,score)
                    print("tile val" , tile)
                    print("player score", player.score)
                    self.assertEqual(player.score, score)
                    print(player.score, score)

             

    def test_out_of_bounds_row(self):
        self.client.post('/game/create')
        response = self.client.post(f'/game/pick/One/{33}/{0}/')
        #print(vars(response))
        #tile = Tile.objects.get(row=-3, col=0)
        self.assertIn('Invalid row or column', response.content.decode())

    
    def test_player_name(self):
        self.client.post('/game/create')
        response = self.client.post(f'/game/pick/Three/{3}/{0}/')
        self.assertIn('No Such Player', response.content.decode())
       
  