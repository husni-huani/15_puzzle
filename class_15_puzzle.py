def puzzle_to_num(puzzle):
    ans = 0
    for row in range(4):
        for column in range(4):
            ans = (ans << 4) + puzzle[row][column]
    return ans

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
        
        self.pos_curr_num = (4,4) # buat posisi block yang mau dipindahin
        
        self.queue = []
        self.seen = []
        self.seen_and_move = []
        
        self.sequence = ''

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
        for row in range(4):
            for column in range(4):
                curr_val = self.val_index(row, column)
                final_pos = (curr_val-1)//4 , (curr_val-1)%4
                if curr_val == 0:
                    final_pos = 3,3
                distance_goal = abs(row-final_pos[0]) + abs(column-final_pos[1])
                score_goal += distance_goal/6            
                
        return score_goal

    def solve_naive(self):
        self.queue.append((self.num_puzzle, self.pos_zero, 0, self.relative_score(), (0,0) ))
        # queue (num_puzzle, pos_zero, step, skor heuristik, (index referensi di self.seen, move) )
        count = 0
        while True:
            count += 1
            if count % 1000 == 0:
                print(count)
            curr_board = self.queue[0]
            curr_num_puzzle = curr_board[0]
            curr_pos_zero = curr_board[1]
            curr_step = curr_board[2]
            curr_reference = curr_board[4]
            self.num_puzzle = curr_num_puzzle
            self.pos_zero = curr_pos_zero
            for move in self.possible_move():
                self.move(move)
                if self.num_puzzle not in self.seen:
                    self.queue.append((self.num_puzzle, self.pos_zero, curr_step+1, (curr_step+1)/120 + self.relative_score(), (len(self.seen), move) ))
                self.num_puzzle = curr_num_puzzle
                self.pos_zero = curr_pos_zero
            self.seen.append(curr_num_puzzle)
            self.seen_and_move.append( (curr_num_puzzle, curr_step, (curr_reference) ) )
            del self.queue[0]
            # seen_and_move (num_puzzle, step, (index referensi, move))
            self.queue.sort(key = lambda x : x[3])
            if self.num_puzzle == self.goal:
                break
        self.show_board()
        self.populate_sequence()

    
    def populate_sequence(self):
        index = len(self.seen_and_move) -1
        move_str = ''
        while index != 0:
            move = self.seen_and_move[index][2][1]
            move_str = str(move) + move_str
            index = self.seen_and_move[index][2][0]
        self.sequence = self.sequence + move_str
    
    def show_sequence(self):
        move_dict = {0 : 'up', 1 : 'down', 2 : 'right', 3 : 'left'}
        move_dict_rev = {0 : 'down', 1 : 'up', 2 : 'left', 3 : 'right'}
        for move in self.sequence:
            print(move_dict_rev[int(move)], end=' ')
    
    def show_sequence_string(self):
        return self.sequence