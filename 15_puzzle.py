def puzzle_to_num(puzzle):
    ans = 0
    for row in range(4):
        for column in range(4):
            ans = (ans << 4) + puzzle[row][column]
    return ans

from os import system
from time import time, sleep

class puzzle_board():
    def __init__(self, puzzle):
        self.num_puzzle = puzzle_to_num(puzzle)
        self.init_state = [(0,0) for i in range(16)]
        for row in range(4):
            for column in range(4):
                if puzzle[row][column] == 0:
                    self.pos_zero = (row, column)
                self.init_state[puzzle[row][column]] = row, column
                
        goal = 0
        for i in range(1,16):
            goal = (goal << 4) + i
        goal = goal << 4
        self.goal = goal


    def val_index(self, row, column):
        pos = (3-row)*16 + (3-column)*4
        return (self.num_puzzle >> pos) & 15
    def show_board(self):
        str_ans = ''
        for row in range(4):
            for column in range(4):
                curr_val = self.val_index(row, column)
                str_ans += str(curr_val) + ' '
            str_ans += '\n'
        print(str_ans)
    def change_block(self, row, column, num):
        pos = (3-row)*16 + (3-column)*4
        back = self.num_puzzle & ((1 << (pos)) -1)
        front = self.num_puzzle >> (pos+4)
        self.num_puzzle = (((front << 4) + num) << pos) + back
    def move_up(self):
        if self.pos_zero[0] == 0:
            return False
        up_index = (self.pos_zero[0]-1, self.pos_zero[1])
        up_val = self.val_index(up_index[0], up_index[1])
        self.change_block(self.pos_zero[0], self.pos_zero[1], up_val)
        self.change_block(up_index[0], up_index[1], 0)
        self.pos_zero = up_index
        return True
    def move_down(self):
        if self.pos_zero[0] == 3:
            return False
        down_index = (self.pos_zero[0]+1, self.pos_zero[1])
        down_val = self.val_index(down_index[0], down_index[1])
        self.change_block(self.pos_zero[0], self.pos_zero[1], down_val)
        self.change_block(down_index[0], down_index[1], 0)
        self.pos_zero = down_index
        return True
    def move_right(self):
        if self.pos_zero[1] == 3:
            return False
        right_index = (self.pos_zero[0], self.pos_zero[1]+1)
        right_val = self.val_index(right_index[0], right_index[1])
        self.change_block(self.pos_zero[0], self.pos_zero[1], right_val)
        self.change_block(right_index[0], right_index[1], 0)
        self.pos_zero = right_index
        return True
    def move_left(self):
        if self.pos_zero[1] == 0:
            return False
        left_index = (self.pos_zero[0], self.pos_zero[1]-1)
        left_val = self.val_index(left_index[0], left_index[1])
        self.change_block(self.pos_zero[0], self.pos_zero[1], left_val)
        self.change_block(left_index[0], left_index[1], 0)
        self.pos_zero = left_index
        return True
    def move(self, move):
        # move -> {0 : up, 1 : down, 2 : right, 3 : left}
        if move == 0:
            return self.move_up()
        elif move == 1:
            return self.move_down()
        elif move == 2:
            return self.move_right()
        elif move == 3:
            return self.move_left()
    def possible_move(self):
        list_ans = []
        if self.pos_zero[0] != 0:
            list_ans.append(0)
        if self.pos_zero[0] != 3:
            list_ans.append(1)
        if self.pos_zero[1] != 3:
            list_ans.append(2)
        if self.pos_zero[1] != 0:
            list_ans.append(3)
        return list_ans
    
    def relative_score(self):
        score_goal = 0
        score_init = 0
        for row in range(4):
            for column in range(4):
                curr_val = self.val_index(row, column)
                final_pos = (curr_val-1)//4 , (curr_val-1)%4
                if curr_val == 0:
                    final_pos = 3,3
                distance_goal = abs(row-final_pos[0]) + abs(column-final_pos[1])
                score_goal += distance_goal/6
                
                distance_init = abs(row-self.init_state[curr_val][0]) + abs(column - self.init_state[curr_val][1])
                score_init += distance_goal/6               
                
        return (score_goal + score_init)/16
    
    def predict_move(self, depth):
        if self.possible_move() == 0:
            return 0, 4
        if depth == 0:
            return self.relative_score(), 4
        list_move = self.possible_move()
        temp_num_puzzle = self.num_puzzle
        temp_pos_zero = self.pos_zero
        score = 1
        pred_move = 4
        for move in list_move:
            self.move(move)
            curr_score = self.predict_move(depth-1)[0]
            score = min(score, curr_score)
            if score == curr_score:
                pred_move = move
            self.num_puzzle = temp_num_puzzle
            self.pos_zero = temp_pos_zero
        return score, pred_move
            
    
    def solve(self):
        predict_depth = 5
        while (self.num_puzzle != self.goal):
            next_move = self.predict_move(predict_depth)
            self.move(next_move[1])
            system('cls')
            self.show_board()
            sleep(0.1)
        
    
    def play(self):
        index = 0
        list_move = [0,2,1,3]
        while True:
            ans = self.move(list_move[index])
            if ans == False:
                if index == 3:
                    index = 0
                else:
                    index += 1
            system('cls')
            self.show_board()
            sleep(0.1)

puzzle = [
    [15, 10, 1, 6],
    [0, 14, 12, 4],
    [5, 3, 2, 13],
    [11, 7, 9, 8]
]

board = puzzle_board(puzzle)
board.solve()