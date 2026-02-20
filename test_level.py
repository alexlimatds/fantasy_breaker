import game as gm
import util, level01, level02, level03, level04

game = gm.Game()
game.player = util.create_player(3)

level04.run(game)