import pyglet

_DEBUG = True

class Widget():
    def __init__(self, game):
        self.game = game
    
    def get_cvar(self, cvar):
        return self.game.get_cvar(cvar)
    
    def draw(self):
        pass

class FPSLabel(Widget, pyglet.text.Label):
    _FORMAT_STR = '%d FPS'
    _UPDATE_RATE_SECONDS = .1
    
    def __init__(self, game):
        Widget.__init__(self, game)
        pyglet.text.Label.__init__(self, anchor_y='bottom')
        pyglet.clock.schedule_interval_soft(self.update_fps, self._UPDATE_RATE_SECONDS)
    
    def draw(self):
        if self.game.get_cvar('dbg_draw_fps'):
            pyglet.text.Label.draw(self)
    
    def update_fps(self, dt):
        fps = pyglet.clock.get_fps()
        self.text = self._FORMAT_STR % (fps + .5)

class DebugLabel(pyglet.text.Label):
    def __init__(self, game):
        Widget.__init__(self, game)
        pyglet.text.Label.__init__(self, 'Game PreAlpha1', anchor_y='bottom')
        self.on_resize(*game.get_size())
    
    def on_resize(self, width, height):
        self.x = width - self.content_width
        self.y = height - self.content_height

class Game(pyglet.window.Window):
    _EVENTS = []
    _BASEEVENTS = ['on_update', 'cvar_changed']
    
    cvars = {}
    _basecvars = {'r_maxfps': 240.0, 'r_vsync': True}
    exclusive_mouse = False
    _widgets = []
    
    def __init__(self):
        self.cvars.update(self._basecvars)
        
        pyglet.window.Window.__init__(self,
            visible=False, caption='Game', vsync=self.get_cvar('r_vsync'),
            resizable=True)
        
        for e in self._EVENTS + self._BASEEVENTS:
            self.register_event_type(e)
        
        self.shedule_update()
    
    def shedule_update(self):
        pyglet.clock.unschedule(self.update)
        pyglet.clock.schedule_interval(self.update, 1.0/self.get_cvar('r_maxfps'))
    
    def add_widget(self, widget):
        self._widgets.append(widget)
        self.push_handlers(widget)
    
    def start(self):
        self.add_widget(FPSLabel(self))
        if _DEBUG:
            self.set_cvar('dbg_draw_fps', True)
            self.add_widget(DebugLabel(self))
        self.set_visible()
        pyglet.app.run()
    
    def set_exclusive_mouse(self, mode):
        self.exclusive_mouse = mode
        pyglet.window.Window.set_exclusive_mouse(self, mode)
    
    def cvar_changed(self, cvar, value):
        if cvar == 'r_fullscreen':
            exclusive_mouse = self.exclusive_mouse
            self.set_exclusive_mouse(True)
            self.set_fullscreen(value)
            self.set_exclusive_mouse(exclusive_mouse)
        elif cvar == 'r_maxfps':
            self.shedule_update()
        elif cvar == 'r_vsync':
            self.set_vsync(value)
    
    def get_cvar(self, cvar):
        return self.cvars.get(cvar)
    
    def set_cvar(self, cvar, value):
        if cvar in self.cvars:
            original = type(self.cvars[cvar])
            new = type(value)
            try:
                value = original(value)
            except ValueError:
                print("Type incorrect, expected %s, got %s" % (original, new))
                return
        self.cvars[cvar] = value
        self.dispatch_event('cvar_changed', cvar, value)
    
    def on_resize(self, width, height):
        pyglet.window.Window.on_resize(self, width, height)
    
    def invert_cvar(self, cvar):
        return self.set_cvar(cvar, not self.get_cvar(cvar))
    
    def on_key_release(self, symbol, modifiers):
        if _DEBUG and symbol == pyglet.window.key.F:
            self.invert_cvar('dbg_draw_fps')
        elif _DEBUG and symbol == pyglet.window.key.F11:
            self.invert_cvar('r_fullscreen')
    
    def update(self, dt):
        self.dispatch_event('on_update', dt)
    
    def on_draw(self):
        if self.get_cvar('_g_clear_on_frame'):
            self.clear()
        for e in self._widgets:
            e.draw()

def forcedebug():
    if not _DEBUG:
        print('Please run via main.py')
        exit(1)

if __name__ == '__main__':
    forcedebug()
    g = Game()
    g.set_cvar('_g_clear_on_frame', True)
    g.start()
