# -*- coding: utf-8

from __future__ import print_function
import os, random, pygame, gamebasics


#______________________________________________________________________________

colormap = {
    1: (  0, 255, 255), # (cyan) 'I' shaped tetrimino blocks
    2: (  0,   0, 255), # (blue) 'J' shaped tetrimino blocks
    3: (255, 140,   0), # (orange) 'L' shaped tetrimino blocks
    4: (255, 255,   0), # (gold) 'O' shaped tetrimino blocks
    5: (  0, 255,   0), # (green) 'S' shaped tetrimino blocks
    6: (255,   0, 255), # (magenta) 'T' shaped tetrimino blocks
    7: (255,   0,   0), # (red) 'Z' shaped tetrimino blocks
    8: (105, 105, 105)  # (gray) obstacles or screen bounds
}


#______________________________________________________________________________

class Tetrimino:
    """A letter-shaped piece composed of four colored blocks. In total, there
    are seven types of tetriminos, defined by their shapes and colors:
    I (cyan), J (blue), L (orange), O (gold), S (green), T (magenta), Z (red).
    """

    matrixmap = {
        # 'I' shaped tetrimino.
        1:[[[0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0]],
           [[0,0,0,0,0],
            [0,0,0,0,0],
            [1,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]],
           [[0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,1,1,1],
            [0,0,0,0,0],
            [0,0,0,0,0]]],
        
        # 'J' shaped tetrimino.
        2:[[[0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,1,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,1,1,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]],

        # 'L' shaped tetrimino.
        3:[[[0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,1,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,1,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,1,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,0,1,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]],

        # 'O' shaped tetrimino.
        4:[[[0,0,0,0,0],
            [0,1,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,1,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,1,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,1,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]],

        # 'S' shaped tetrimino.
        5:[[[0,0,0,0,0],
            [0,1,0,0,0],
            [0,1,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,1,1,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,1,0],
            [0,0,0,1,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,1,1,0],
            [0,1,1,0,0],
            [0,0,0,0,0]]],

        # 'T' shaped tetrimino.
        6:[[[0,0,0,0,0],
            [0,0,1,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,1,0,0],
            [0,1,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0]]],

        # 'Z' shaped tetrimino.
        7:[[[0,0,0,0,0],
            [0,0,1,0,0],
            [0,1,1,0,0],
            [0,1,0,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,1,0,0],
            [0,0,1,1,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,0,0,1,0],
            [0,0,1,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0]],
           [[0,0,0,0,0],
            [0,1,1,0,0],
            [0,0,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]]
    }


    def __init__(self, id, middle=5):
        """Tetrimino constructor. Sets the data matrix according to the given
        id and also places the tetrimino at its initial position.
        """
        self.id     = id
        self.angle  = 0
        self.row    = 0
        self.col    = middle - 1
        self.matrix = Tetrimino.matrixmap[self.id]


    def move(self, direction):
        """Move the tetrimino one position to the left (direction == -1) or to
        the right (direction == 1).
        """
        if direction == -1:
            self.col -= 1
        elif direction == 1:
            self.col += 1


    def fall(self):
        """Move the tetrimino one position down.
        """
        self.row += 1


    def rotate(self, clockwise=True):
        """Changes the tetrimino's rotation angle (+ or - 90 degrees).
        """
        if clockwise:
            self.angle = (self.angle + 90) % 360
        else:
            self.angle = (self.angle - 90) % 360



#______________________________________________________________________________

class TetrisScene(gamebasics.Scene, object):
    """Scene subclass specifically built for controlling the Tetris gameplay.
    """

    def __init__(self, game, gridsize=(20, 10)):
        """See the docs for gamebasics.Scene.__init__.
        """
        super(TetrisScene, self).__init__(game)
        
        self.gridsize       = gridsize[0] + 2, gridsize[1] + 2
        self.speedlevel     = 1
        self.score          = 0
        self.lines          = 0
        self.running        = False
        self.paused         = False
        self.currtetri      = None
        self.nexttetri      = None
        self.movedelay      = 0
        self.movedelaymax   = 3
        self.falldelay      = 0
        self.falldelaymax   = 2
        self.rotatedelay    = 0
        self.rotatedelaymax = 4
        self.refertime      = 0
        self.accumtime      = 0
        self.currmusic      = 1
        self.musics         = []
        self.grid           = None

        # pygame.key.set_repeat(1, 75)


    def newgame(self, speedlevel=1):
        """Begins a new gameplay. Initializes the statistics (score, speed
        level, etc), builds an empty grid (with obstacles at the corners) and
        sets a timer which regularly calls the update method.
        """
        self.speedlevel  = speedlevel
        self.score       = 0
        self.lines       = 0
        self.running     = True
        self.paused      = False
        self.movedelay   = 0
        self.falldelay   = 0
        self.rotatedelay = 0

        middle = (self.gridsize[1] - 2) / 2
        self.currtetri  = Tetrimino(random.randint(1, 7), middle)
        self.nexttetri  = Tetrimino(random.randint(1, 7), middle)

        self.grid = [0] * self.gridsize[0]
        for i in range(self.gridsize[0]):
            self.grid[i] = [0] * self.gridsize[1]
            for j in range(self.gridsize[1]):
                if i == 0 or i == self.gridsize[0] - 1 or \
                   j == 0 or j == self.gridsize[1] - 1:
                    self.grid[i][j] = 8 # obstacle block

        pygame.mixer.music.play(-1)

        self.set_speedlevel(self.speedlevel)
        self.refertime = pygame.time.get_ticks()
        self.accumtime = 0


    def toggle_pause(self):
        """Pauses/unpauses the gameplay.
        """
        if self.running:
            self.paused = not self.paused
            self.get_timer('TimedUpdate').toggle_pause()
            self.get_resource('sound', 'PauseSound').play()

            if self.paused:
                self.accumtime += pygame.time.get_ticks() - self.refertime
                pygame.mixer.music.pause()
            else:
                self.refertime = pygame.time.get_ticks()
                pygame.mixer.music.unpause()


    def switch_music(self, inc):
        """Switches the background music.
        """
        self.currmusic = (self.currmusic + inc) % len(self.musics)
        if self.currmusic == 0:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.load(self.musics[self.currmusic])
            pygame.mixer.music.play(-1)


    def get_elapsed_time(self):
        """Returns the time elapsed since the beginning of the gameplay (not
        including paused time).
        """
        return pygame.time.get_ticks() - self.refertime + self.accumtime


    def timedupdate(self):
        """Callback function for the main timer. It basically controls the
        scene logic, by calling the methods that make the tetrimino fall, check
        for collisions, find completed rows, attach blocks, increase the score,
        etc. The number of times this method is called per second depends on
        the game's speed level.
        """
        self.currtetri.fall()
        if self.collision():
            self.currtetri.row -= 1
            self.attach()

            boundmin = max(self.currtetri.row, 1)
            boundmax = min(self.currtetri.row + 5, self.gridsize[0]-1)
            completed = self.find_completed_rows((boundmin, boundmax))
            consecutives = self.find_consecutives(completed)

            for row in completed:
                self.clear_row(row)
            for count in consecutives:
                bonus = 100 * (count + 1)**2 if count + 1 < 4 else 2000
                self.score += bonus

            if completed:
                self.lines += len(completed)
                if self.lines >= 12*self.speedlevel - 2:
                    self.set_speedlevel(self.speedlevel + 1)
                self.get_resource('sound', 'ScoreSound').play()
            else:
                self.get_resource('sound', 'CrashSound').play()

            if self.game_is_lost():
                self.gameover()
            else:
                middle = (self.gridsize[1] - 2) / 2
                self.currtetri = self.nexttetri
                self.nexttetri = Tetrimino(random.randint(1, 7), middle)


    def move(self, direction):
        """Move the current tetrimino one position to the left or to the right
        if there is no collision with any other block.
        """
        self.currtetri.move(direction)
        if self.collision():
            self.currtetri.move(-direction)


    def quickfall(self):
        """Quickly sends the current tetrimino down the grid.
        """
        self.currtetri.fall()
        if self.collision():
            self.currtetri.row -= 1

        # while not self.collision():
        #     self.currtetri.fall()
        # self.currtetri.row -= 1


    def rotate(self):
        """Changes the current tetrimino's rotation angle if there is no
        collision with any other block.
        """
        self.currtetri.rotate()
        if self.collision():
            self.currtetri.rotate(False)
        else:
            self.get_resource('sound', 'RotateSound').play()


    def collision(self):
        """Tests whether the current tetrimino has collided with any other
        block of the grid.
        """
        t = self.currtetri
        a = t.angle / 90
        for i in range(5):
            for j in range(5):
                if t.matrix[a][i][j] and self.grid[i + t.row][j + t.col]:
                    return True
        return False


    def find_completed_rows(self, bounds):
        """Finds grid rows which were completely filled by tetrimino blocks.
        """
        result = []
        for i in range(bounds[0], bounds[1]):
            if 0 not in self.grid[i]:
                result.append(i)
        return result


    def clear_row(self, row):
        """Removes all blocks from completed rows and sends all blocks above
        one position below.
        """
        for i in range(row, 1, -1):
            self.grid[i] = self.grid[i - 1]
        self.grid[1] = [8] + [0]*(self.gridsize[1] - 2) + [8]


    def find_consecutives(self, sortedlist):
        """Counts the lengths of all sequences of consecutive numbers found in
        a sorted list, returning these counts in another list.
        """
        countlist = []
        previous = None
        count = 0
        for num in sortedlist:
            if previous:
                if previous == num - 1:
                    count += 1
                else:
                    countlist.append(count)
                    count = 0
            previous = num
        if previous:
            countlist.append(count)
        return countlist


    def attach(self):
        """Attaches the current tetrimino's blocks to the grid.
        """
        t = self.currtetri
        a = t.angle / 90
        for i in range(5):
            for j in range(5):
                if t.matrix[a][i][j]:
                    self.grid[i + t.row][j + t.col] = t.id


    def set_speedlevel(self, speedlevel):
        """Sets a new speed level and adjust the timer interval.
        """
        self.speedlevel = speedlevel
        interv = [500, 400, 300, 200, 150, 100, 75, 50, 25, 10]

        timer = self.get_timer('TimedUpdate')
        if timer:
            timer.interval = interv[min(self.speedlevel-1, len(interv)-1)]
        else:
            timer = gamebasics.Timer(interv[self.speedlevel], self.timedupdate)
            self.add_timer('TimedUpdate', timer)


    def game_is_lost(self):
        """Tests whether the player has lost the game (there is any block in
        the first upper visible row.
        """
        for block in self.grid[1][1:self.gridsize[1]-1]:
            if block:
                return True
        return False


    def gameover(self):
        """Finishes the gameplay (not the game program as a whole).
        """
        self.paused  = False
        self.running = False
        self.del_timer('TimedUpdate')
        pygame.mixer.music.fadeout(1000)
        print('Game Over')


    # Overridden methods -----------------------------------------------------

    def load(self):
        """See the docs for gamebasics.Scene.load.
        """
        filename = os.path.join('fonts', 'thirteen-pixel-fonts.regular.ttf')
        titlefont = pygame.font.Font(filename, 54)
        self.add_resource('font', 'TitleFont', titlefont)

        filename = os.path.join('fonts', 'pixel-millennium.regular.ttf')
        labelfont = pygame.font.Font(filename, 32)
        self.add_resource('font', 'LabelFont', labelfont)

        filename = os.path.join('sound', 'crash.wav')
        crashsound = pygame.mixer.Sound(filename)
        self.add_resource('sound', 'CrashSound', crashsound)

        filename = os.path.join('sound', 'pause.wav')
        pausesound = pygame.mixer.Sound(filename)
        self.add_resource('sound', 'PauseSound', pausesound)

        filename = os.path.join('sound', 'rotate.wav')
        rotatesound = pygame.mixer.Sound(filename)
        self.add_resource('sound', 'RotateSound', rotatesound)

        filename = os.path.join('sound', 'score.wav')
        scoresound = pygame.mixer.Sound(filename)
        self.add_resource('sound', 'ScoreSound', scoresound)

        self.musics = ['', # no music
                       os.path.join('music', 'Tetris1.mp3'),
                       os.path.join('music', 'Tetris2.mp3')]
        filename = self.musics[self.currmusic]
        pygame.mixer.music.load(filename)


    def handle_user_events(self, events):
        """See the docs for gamebasics.Scene.handle_user_events.
        """
        if not self.running:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.toggle_pause()
                elif not self.paused:
                    if event.key == pygame.K_m:
                        self.switch_music(1)
                    elif event.key == pygame.K_n:
                        self.switch_music(-1)
                # elif event.key == pygame.K_UP:
                #     self.currtetri.rotate()
                # elif event.key == pygame.K_DOWN:
                #     self.quickfall()
                # elif event.key == pygame.K_LEFT:
                #     self.currtetri.move(-1)
                # elif event.key == pygame.K_RIGHT:
                #     self.currtetri.move(1)

        if not self.paused:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                if self.rotatedelay == 0:
                    self.rotate()
                    self.rotatedelay = self.rotatedelaymax
                self.rotatedelay -= 1
            elif pressed[pygame.K_DOWN]:
                if self.falldelay == 0:
                    self.quickfall()
                    self.falldelay = self.falldelaymax
                self.falldelay -= 1
            elif pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT]:
                if self.movedelay == 0:
                    self.move(-1)
                    self.movedelay = self.movedelaymax
                self.movedelay -= 1
            elif pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                if self.movedelay == 0:
                    self.move(1)
                    self.movedelay = self.movedelaymax
                self.movedelay -= 1


    def update(self):
        """See the docs for gamebasics.Scene.update.
        """
        pass # Nothing to be done since we only need to update the game logic
             # when the timer events happen.


    def draw(self):
        """See the docs for gamebasics.Scene.draw.
        """
        if not self.running or self.paused:
            return
        
        blockrect = pygame.Rect(
            0,                          # x
            0,                          # y
            300 / self.gridsize[1] - 1, # width
            550 / self.gridsize[0] - 1  # height
        )
        black = (  0,   0,   0)
        white = (255, 255, 255)

        # Clear screen.
        self.game.screen.fill(black)

        # Draw the title label.
        titlefont = self.get_resource('font', 'TitleFont')
        titlesurf = titlefont.render('JATC', True, white)
        xpos = (275 - titlesurf.get_width()) / 2
        self.game.screen.blit(titlesurf, (xpos, 10))
        # titlesurf1 = titlefont.render('TETRIS', True, white)
        # xpos = (275 - titlesurf1.get_width()) / 2
        # self.game.screen.blit(titlesurf1, (xpos, 5))
        # titlesurf2 = titlefont.render('CLONE', True, white)
        # xpos = (275 - titlesurf2.get_width()) / 2
        # self.game.screen.blit(titlesurf2, (xpos, 50))

        # Draw the next tetrimino label.
        labelfont = self.get_resource('font', 'LabelFont')
        nextsurf = labelfont.render('NEXT', True, white)
        xpos = (275 - nextsurf.get_width()) / 2
        self.game.screen.blit(nextsurf, (xpos, 100))

        # Draw the score labels.
        scoresurf1 = labelfont.render('SCORE', True, white)
        xpos = (275 - scoresurf1.get_width()) / 2
        self.game.screen.blit(scoresurf1, (xpos, 305))

        scoresurf2 = labelfont.render(str(self.score), True, white)
        xpos = (275 - scoresurf2.get_width()) / 2
        self.game.screen.blit(scoresurf2, (xpos, 340))

        # Draw the speed level labels.
        levelsurf1 = labelfont.render('LEVEL', True, white)
        xpos = (275 - levelsurf1.get_width()) / 2
        self.game.screen.blit(levelsurf1, (xpos, 385))

        levelsurf2 = labelfont.render(str(self.speedlevel), True, white)
        xpos = (275 - levelsurf2.get_width()) / 2
        self.game.screen.blit(levelsurf2, (xpos, 420))

        # Draw the time labels.
        timesurf1 = labelfont.render('TIME', True, white)
        xpos = (275 - timesurf1.get_width()) / 2
        self.game.screen.blit(timesurf1, (xpos, 465))

        milliseconds = self.get_elapsed_time()
        hours        = milliseconds / 3600000 % 24
        minutes      = milliseconds / 60000 % 60
        seconds      = milliseconds / 1000 % 60
        formattime   = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

        timesurf2 = labelfont.render(formattime, True, white)
        xpos = (275 - timesurf2.get_width()) / 2
        self.game.screen.blit(timesurf2, (xpos, 500))

        # Draw the next tetrimino background square.
        square = pygame.Rect(75, 95, 125, 190)
        pygame.draw.rect(self.game.screen, white, square, 1)

        # # Draw the grid blocks.
        # for i in range(self.gridsize[0]):
        #     for j in range(self.gridsize[1]):
        #         if self.grid[i][j]:
        #             blockcolor = colormap[self.grid[i][j]]
        #             blockrect.x = j * (blockrect.width + 1) + 250
        #             blockrect.y = i * (blockrect.height + 1)
        #             pygame.draw.rect(self.game.screen, blockcolor, blockrect)

        # Draw the grid background square.
        square = pygame.Rect(274, 24, 251, 501)
        pygame.draw.rect(self.game.screen, white, square, 1)

        # Draw the grid blocks.
        for i in range(1, self.gridsize[0] - 1):
            for j in range(1, self.gridsize[1] - 1):
                if self.grid[i][j]:
                    blockcolor = colormap[self.grid[i][j]]
                    blockrect.x = j * (blockrect.width + 1) + 250
                    blockrect.y = i * (blockrect.height + 1)
                    pygame.draw.rect(self.game.screen, blockcolor, blockrect)

        # Draw the current tetrimino.
        t = self.currtetri
        a = t.angle / 90
        for i in range(5):
            for j in range(5):
                if t.matrix[a][i][j]:
                    blockcolor  = colormap[t.id]
                    blockrect.x = (j + t.col) * (blockrect.width + 1) + 250
                    blockrect.y = (i + t.row) * (blockrect.height + 1)
                    pygame.draw.rect(self.game.screen, blockcolor, blockrect)

        # Draw the next tetrimino.
        blockrect.width = blockrect.height = 24
        t = self.nexttetri
        a = t.angle / 90
        for i in range(5):
            for j in range(5):
                if t.matrix[a][i][j]:
                    blockcolor  = colormap[t.id]
                    blockrect.x = j * (blockrect.width + 1)  + 75
                    blockrect.y = i * (blockrect.height + 1) + 130
                    pygame.draw.rect(self.game.screen, blockcolor, blockrect)



#______________________________________________________________________________

class TetrisGame(gamebasics.Game, object):
    """Game subclass for Tetris. For now, it only contains one scene (for the
    gameplay itself), but later a title/menu screen might be included too.
    """

    def __init__(self, gridsize):
        """See the docs for gamebasics.Game.__init__.
        """
        super(TetrisGame, self).__init__(
            title='Just Another Tetris Clone',
            screensize=(550, 550),
            framerate=30)
        
        self.add_scene('gameplay', TetrisScene(self, gridsize))
        self.goto_scene('gameplay')
        self.currscene.newgame()


#______________________________________________________________________________


if __name__ == '__main__':
    import sys

    gridrows = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    gridcols = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    TetrisGame((gridrows, gridcols)).start()
