
import math
import time
import random
import base64
import matplotlib
from tkinter import *
from urllib.request import urlopen

#matplotlib.use('TkAgg')

class GameVisualization:
    def __init__(self, num_players, width, height, delay = 0.2):
        "Initializes a visualization with the specified parameters."
        # Number of seconds to pause after each frame
        self.delay = delay

        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.num_players = num_players

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gray squares for dusty tiles
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                if (i, j) not in self.tiles:
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2,
                                                                 fill = "black")
                else:
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2,
                                                                   fill = "red")


        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

        # Draw some status text
        self.players = None
        
        self.time = 0

        # Bring window to front and focus
        self.master.attributes("-topmost", True)  # Brings simulation window to front upon creation
        self.master.focus_force()                 # Makes simulation window active window
        self.master.attributes("-topmost", False) # Allows you to bring other windows to front

        self.master.update()



    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_player(self, position, direction, player):
        "Returns a polygon representing a player with the specified parameters."
        x, y = position.get_x(), position.get_y()
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y-.25)
        
        
        return self.w.create_text(x1, y1, text = player.get_name(), fill="black")

    def update(self, room, players):
        "Redraws the visualization with the specified room and player state."

        # Delete all unfurnished tiles
        for tile in self.tiles:
            self.w.delete(self.tiles[tile])

        # Redraw item spaces
        self.tiles = {}
        for i in range(self.width):
            for j in range(self.height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                if not room.is_tile_cleaned(i, j):
                    #get dust amount
                    dustAmount = room.get_dust_amount(i, j)
                    color = 150
                    color = int(color/dustAmount)
                    r = color
                    g = color
                    b = color
                    rgb = r, g, b
                    Hex = '#%02x%02x%02x' % rgb
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = str(Hex))

        # Delete all existing players.
        if self.players:
            for player in self.players:
                self.w.delete(player)
                self.master.update_idletasks()
        # Draw new players
        self.players = []
        for player in players:
            pos = player.get_position()
            x, y = pos.get_x(), pos.get_y()
            x1, y1 = self._map_coords(x - 0.04, y - 0.04)
            x2, y2 = self._map_coords(x + 0.04, y + 0.04)
            self.players.append(self.w.create_oval(x1, y1, x2, y2,
                                                  fill = "", outline = 'black'))
            self.players.append(
                self._draw_player(player.get_position(), player.get_direction(), player))
        # Update text
        self.time += 1
        
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()
