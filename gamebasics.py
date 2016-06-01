# -*- coding: utf-8

"""Copyright (c) 2016, Carlos Henrique Villa Pinto
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.

"""

import pygame


#______________________________________________________________________________

class Game:
    """Basic game superclass.
    A game is composed of multiple named and interchangeable scenes, where only
    one is executed at a time. Most methods in this class just delegate tasks
    to the current scene in execution.
    """

    def __init__(self, title='', screensize=(640,480), framerate=30):
        """Game constructor. It initializes pygame as well as some basic state
        variables and collections.
        """
        self.title        = title
        self.screensize   = screensize
        self.framerate    = framerate
        self.frametime    = 1000 / framerate
        self.lastticks    = 0
        self.currscene    = None
        self.running      = False
        self.scenes       = {}
        self.globaltimers = {}

        pygame.init()
        self.screen = pygame.display.set_mode(self.screensize)
        pygame.display.set_caption(self.title)


    def add_scene(self, scenename, scene):
        """Adds a named scene to the game.
        """
        self.scenes.update({scenename: scene})


    def del_scene(self, scenename):
        """Deletes a named scene from the game.
        """
        self.scenes.pop(scenename)


    def get_scene(self, scenename):
        """Gets a named scene of the game.
        """
        return self.scenes.get(scenename)


    def goto_scene(self, scenename):
        """Change the game execution to another existing scene.
        """
        self.currscene and self.currscene.unload()
        self.currscene = self.scenes.get(scenename)
        self.currscene.load()


    def add_globaltimer(self, timername, timer):
        """Adds a named global timer to the game.
        """
        self.globaltimers.update({timername: timer})


    def del_globaltimer(self, timername):
        """Deletes a named global timer from the game.
        """
        self.globaltimers.pop(timername)


    def get_globaltimer(self, timername):
        """Gets a named global timer of the scene.
        """
        return self.globaltimers.get(timername)


    def start(self):
        """Starts the main loop of the game.
        """
        self.running = True
        self.mainloop()


    def quit(self):
        """Quits the game by stopping the main loop.
        """
        self.running = False


    def handle_user_events(self):
        """Handles global user events that can happen at any scene.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()

        self.currscene and self.currscene.handle_user_events(events)


    def handle_timer_events(self):
        """Handles gobal timer events that can happen at any scene.
        """
        for timername, timer in self.globaltimers.items():
            if timer.paused:
                continue
            elapsedtime = pygame.time.get_ticks() - timer.lastcall
            if elapsedtime >= timer.interval:
                timer.callback(timer.arguments) if timer.arguments else \
                    timer.callback()
                if timername in self.globaltimers:
                    self.globaltimers[timername].lastcall = pygame.time.get_ticks()

        self.currscene and self.currscene.handle_timer_events()


    def update(self):
        """Updates the game logic.
        """
        self.currscene and self.currscene.update()


    def draw(self):
        """Draws all graphical elements (sprites, BGs, texts, etc) on the screen.
        """
        self.currscene and self.currscene.draw()
        pygame.display.update()


    def delay(self):
        """Delays the main loop so that the game runs at the chosen frame rate.
        """
        elapsedtime = pygame.time.get_ticks() - self.lastticks
        if elapsedtime < self.frametime:
            pygame.time.delay(self.frametime - elapsedtime)
        self.lastticks = pygame.time.get_ticks()


    def mainloop(self):
        """Main loop of the game. It keeps running until the program finishes.
        """
        while self.running:
            self.handle_user_events()
            self.handle_timer_events()
            self.update()
            self.draw()
            self.delay()
        self.currscene and self.currscene.unload()



#______________________________________________________________________________

class Scene:
    """Basic scene superclass.
    A scene has its own logic, events, state and methods. Things like the title
    screen, options screen, as well as each game room/stage, are all individual
    scenes. Most methods in this class must be overwritten by its subclasses.
    """

    def __init__(self, game):
        """Scene constructor. It sets the parent game the scene belongs to and
        initializes the resource (images, sounds, fonts) and timer collections.
        """
        self.game      = game
        self.timers    = {}
        self.resources = {
            'image': {},
            'sound': {},
            'font' : {}
        }


    def add_resource(self, resourcetype, resourcename, resource):
        """Adds a named resource to the scene.
        """
        self.resources[resourcetype].update({resourcename: resource})


    def del_resource(self, resourcetype, resourcename):
        """Deletes a named resource from the scene.
        """
        self.resources[resourcetype].pop(resourcename)


    def get_resource(self, resourcetype, resourcename):
        """Gets a named resource of the scene.
        """
        return self.resources[resourcetype].get(resourcename)


    def add_timer(self, timername, timer):
        """Adds a named timer to the scene.
        """
        self.timers.update({timername: timer})


    def del_timer(self, timername):
        """Deletes a named timer from the scene.
        """
        self.timers.pop(timername)


    def get_timer(self, timername):
        """Gets a named timer of the scene.
        """
        return self.timers.get(timername)


    def unload(self):
        """Unloads the scene resources.
        """
        self.resources.clear()


    def handle_timer_events(self):
        """Handles timer events that are specific for the scene.
        """
        for timername, timer in self.timers.items():
            if timer.paused:
                continue
            elapsedtime = pygame.time.get_ticks() - timer.lastcall
            if elapsedtime >= timer.interval:
                timer.callback(timer.arguments) if timer.arguments else \
                    timer.callback()
                if timername in self.timers:
                    self.timers[timername].lastcall = pygame.time.get_ticks()


    # Abstract methods --------------------------------------------------------

    def load(self):
        """Loads the scene resources.
        """
        raise NotImplementedError('Subclass must implement abstract method')


    def handle_user_events(self, events):
        """Handles user events that are specific for the scene.
        """
        raise NotImplementedError('Subclass must implement abstract method')


    def update(self):
        """Updates the scene logic.
        """
        raise NotImplementedError('Subclass must implement abstract method')


    def draw(self):
        """Draws all graphical elements (sprites, BGs, texts, etc) on the screen.
        """
        raise NotImplementedError('Subclass must implement abstract method')



#______________________________________________________________________________

class Timer(object):
    """A timer defined in terms of a time interval and a callback function that
    is called every time such interval passes. If the callback function has any
    arguments, they should be passed in a dict.
    """

    def __init__(self, interval, callback, arguments=None):
        """Timer constructor. It sets the interval and the callback function.
        """
        super(Timer, self).__init__()
        self.interval  = interval
        self.callback  = callback
        self.arguments = arguments
        self.paused    = False
        self.lastcall  = pygame.time.get_ticks()


    def toggle_pause(self):
        """Just toggles the paused state of the timer. 
        """
        self.paused = not self.paused
