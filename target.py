from pyglet.gl import *
import game

class GameDisplay(game.Widget):
    def __init__(self, game):
        game.Widget.__init__(self, game)
        terrai
    
    def draw(self):
        self.frame_start()
        
        self.frame_end()
    
    def frame_start(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        width, height = self.game.get_size()
        gluPerspective(self.get_cvar('r_fov'), width / height, 0.01, 100.0)
    
    def frame_end(self):
        glPopMatrix()

class Target(game.Game):
    cvars = {
        'r_fov': 45.0,
        '_g_clear_on_frame': True
    }
    
    def __init__(self):
        game.Game.__init__(self)
        self.add_widget(GameDisplay(self))

if __name__ == '__main__':
    game.forcedebug()
    t = Target()
    t.start()
