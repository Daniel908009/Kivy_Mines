from kivy.uix.gridlayout import accumulate
from kivy.uix.actionbar import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import random







# this is the Mine class for the grid buttons
class MineButton(Button):
    # method that gives the button all the info it needs
    def info(self, id, caller, position):
        self.caller = caller
        self.id = id
        self.position = position
    # method that is called when the button is pressed
    def press(self):
        if self.position in self.caller.mines:
            print("You lost")
        elif self.position not in self.caller.all_buttons_revealed:
            self.reveal()
    # method that reveals all the number mine buttons around this one
    def reveal(self):
        buttons_to_reveal = []
        for x in range(self.position[0]-1, self.position[0]+2):
            for y in range(self.position[1]-1, self.position[1]+2):
                if x >= 0 and x < self.caller.number_of_columns and y >= 0 and y < self.caller.number_of_rows and self.caller.grid[x][y] != "X":
                    all_buttons = self.caller.ids.grid.children
                    for button in all_buttons:
                        if button.position == [x,y] and button.position:
                            if str(self.caller.grid[x][y]) != "0":
                                button.text = str(self.caller.grid[x][y])
                            button.background_color = (1,1,1,1)
                            if button.text != "0" and button.position not in self.caller.all_buttons_revealed:
                                print(button.position)
                                buttons_to_reveal.append(button)
        self.caller.all_buttons_revealed.append(self.position)
        for button in buttons_to_reveal:
            button.reveal()

# this is the main grid class used to contain the mine buttons
class MainGrid(GridLayout):
    # method that fils the grid with mine buttons and creates all the diferent arrays
    def start_game(self,width,height,mine_number):
        if hasattr(self, "time"):
            Clock.unschedule(self.time_update)
        self.time = 0
        Clock.schedule_interval(self.time_update, 1)
        self.all_buttons_revealed = []
        self.ids.time_label.text = "00:00:00"
        self.ids.grid.clear_widgets()
        self.number_of_columns = width
        self.number_of_rows = height
        self.number_of_mines = mine_number
        self.ids.grid.cols = width
        # creating the coords of the mines
        self.mines = []
        for i in range(mine_number):
            mine_row = random.randint(1,width-1)
            mine_col = random.randint(1,height-1)# top left corner will always be safe
            while [mine_row,mine_col] in self.mines: 
                mine_row = random.randint(0,width-1)
                mine_col = random.randint(0,height-1)
            self.mines.append([mine_row,mine_col])
        # creating the buttons
        id_number = 0
        for i in range(width):
            for j in range(height):
                button = MineButton()
                button.info(id_number, self, [i,j])
                self.ids.grid.add_widget(button)
                id_number += 1
        # creating the numbers map
        self.grid = []
        for i in range(width):
            self.grid.append([])
            for j in range(height):
                if [i,j] in self.mines:
                    self.grid[i].append("X")
                else:
                    # getting the number of mines around
                    mines_around = 0
                    for x in range(i-1, i+2):
                        for y in range(j-1, j+2):
                            if [x,y] in self.mines:
                                mines_around += 1
                    self.grid[i].append(mines_around)

    def time_update(self,dt):
        self.time += dt
        hours = int(self.time/3600)
        minutes = int((self.time - hours*3600)/60)
        seconds = int(self.time - hours*3600 - minutes*60)
        self.ids.time_label.text = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

# this is the main app class
class MinesApp(App):
    def build(self):
        return MainGrid()
    
# running the app
if __name__ == '__main__':
    MinesApp().run()