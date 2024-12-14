from kivy.uix.actionbar import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import random








class MineButton(Button):
    def info(self, id, caller, position):
        self.caller = caller
        self.id = id
        self.position = position
        if [position[0],position[1]] in self.caller.mines:
            self.text = "X"



class MainGrid(GridLayout):
    def start_game(self,width,height,mine_number):
        self.ids.grid.clear_widgets()
        self.number_of_columns = width
        self.number_of_rows = height
        self.number_of_mines = mine_number
        self.ids.grid.cols = width
        # creating the coords of the mines
        for i in range(mine_number):
            mine_row = random.randint(0,width-1)
            mine_col = random.randint(0,height-1)
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
        for i in range(width):
            self.grid.append([])
            for j in range(height):
                if [i,j] in self.mines:
                    self.grid[i].append("X")
                else:
                    # getting the number of mines around
                    mines_around = 0
                    for x in range(i-1, i+1):
                        for y in range(j-1, j+1):
                            if [x,y] in self.mines:
                                mines_around += 1
                    self.grid[i].append(mines_around)
        #print(self.grid)

class MinesApp(App):
    def build(self):
        return MainGrid()

if __name__ == '__main__':
    MinesApp().run()