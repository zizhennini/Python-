import random
import turtle


class BackGround(turtle.Turtle):
    block_pos = [(-150, 110), (-50, 110), (50, 110), (150, 110),
                 (-150, 10), (-50, 10), (50, 10), (150, 10),
                 (-150, -90), (-50, -90), (50, -90), (150, -90),
                 (-150, -190), (-50, -190), (50, -190), (150, -190)]

    def __init__(self):
        super().__init__()
        self.penup()
        self.ht()
        self.text_is_clear = True
        self.top_score = 0
        self.turtle_show_score = turtle.Turtle()
        self.turtle_show_text = turtle.Turtle()
        try:
            with open('score.txt', 'r') as f:
                self.top_score = int(f.read())
        except (FileNotFoundError, ValueError):
            self.top_score = 0
        self.draw_back_ground()

    def draw_back_ground(self):
        # 绘制背景方块
        self.color("#bbada0")
        self.shape("square")
        self.shapesize(4.5, 4.5)
        for pos in self.block_pos:
            self.goto(pos)
            self.stamp()

        # 绘制顶部装饰条
        self.color("#8f7a66")
        self.goto(0, 210)
        self.shapesize(0.8, 22)
        self.stamp()

        # 显示文字标签
        self.turtle_show_score.penup()
        self.turtle_show_score.ht()
        self.turtle_show_score.color("white")
        self.turtle_show_score.goto(-120, 175)
        self.turtle_show_score.write("0", align="center", font=("Arial", 20, "bold"))
        self.turtle_show_score.goto(115, 175)
        self.turtle_show_score.write(f"{self.top_score}", align="center", font=("Arial", 20, "bold"))

        self.turtle_show_text.penup()
        self.turtle_show_text.ht()
        self.turtle_show_text.color("#8f7a66")
        self.turtle_show_text.goto(-120, 220)
        self.turtle_show_text.write("Score", align="center", font=("Arial", 14, "bold"))
        self.turtle_show_text.goto(115, 220)
        self.turtle_show_text.write("Best", align="center", font=("Arial", 14, "bold"))

    def show_score(self, score):
        if score > self.top_score:
            self.top_score = score
            with open('score.txt', 'w') as f:
                f.write(f"{self.top_score}")
        self.turtle_show_score.clear()
        self.turtle_show_score.write(f"{score}", align="center", font=("Arial", 20, "bold"))
        self.turtle_show_score.goto(115, 175)
        self.turtle_show_score.write(f"{self.top_score}", align="center", font=("Arial", 20, "bold"))

    def show_win_lose(self, win):
        self.turtle_show_text.clear()
        self.turtle_show_text.color("#8f7a66")
        self.turtle_show_text.goto(0, 0)
        if win:
            self.turtle_show_text.write("You Win!\nPress SPACE to restart", align="center", font=("Arial", 24, "bold"))
        else:
            self.turtle_show_text.write("Game Over!\nPress SPACE to restart", align="center",
                                        font=("Arial", 24, "bold"))
        self.text_is_clear = False


class Block(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.penup()
        self.num = 0
        self.shape("square")
        self.shapesize(4.5, 4.5)

    def draw(self):
        self.clear()
        if self.num > 0:
            colors = {
                2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                1024: "#edc53f", 2048: "#edc22e", 4096: "#a3d7a3",
                8192: "#8cd38c", 16384: "#5cb85c"
            }
            self.color(colors.get(self.num, "#000000"))
            self.stamp()
            self.goto(self.xcor(), self.ycor() - 15)
            self.color("#776e65" if self.num < 8 else "#f9f6f2")
            self.write(str(self.num), align="center", font=("Arial", 24, "bold"))
            self.goto(self.xcor(), self.ycor() + 15)


class Game:
    def __init__(self):
        self.background = BackGround()
        self.score = 0
        self.is_win = True
        self.block_turtle_dict = {}
        for pos in BackGround.block_pos:
            block = Block()
            block.goto(pos)
            self.block_turtle_dict[pos] = block
        self.new_num()

    def check_win_lose(self):
        if all(block.num != 0 for block in self.block_turtle_dict.values()) and \
                not any(self.can_merge(pos) for pos in BackGround.block_pos):
            self.background.show_win_lose(False)
        for block in self.block_turtle_dict.values():
            if block.num == 2048 and self.is_win:
                self.background.show_win_lose(True)
                self.is_win = False

    def can_merge(self, pos):
        current = self.block_turtle_dict[pos].num
        neighbors = []
        x, y = pos
        for dx, dy in [(100, 0), (-100, 0), (0, 100), (0, -100)]:
            neighbor = (x + dx, y + dy)
            if neighbor in self.block_turtle_dict:
                neighbors.append(self.block_turtle_dict[neighbor].num)
        return current in neighbors

    def new_num(self):
        empty_blocks = [block for block in self.block_turtle_dict.values() if block.num == 0]
        if empty_blocks:
            turtle_choice = random.choice(empty_blocks)
            turtle_choice.num = random.choice([2, 2, 2, 2, 4])
            turtle_choice.draw()
            self.background.show_score(self.score)
            self.check_win_lose()

    def move(self, pos_list):
        nums = [self.block_turtle_dict[pos].num for pos in pos_list]
        new_nums, moved = self.merge(nums)
        if moved:
            for pos, num in zip(pos_list, new_nums):
                self.block_turtle_dict[pos].num = num
                self.block_turtle_dict[pos].draw()
        return moved

    def merge(self, nums):
        non_zero = [num for num in nums if num != 0]
        new_nums = []
        skip = False
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                new_nums.append(non_zero[i] * 2)
                self.score += non_zero[i] * 2
                skip = True
            else:
                new_nums.append(non_zero[i])
        new_nums += [0] * (len(nums) - len(new_nums))
        return new_nums, new_nums != nums

    def move_up(self):
        cols = [BackGround.block_pos[i::4] for i in range(4)]
        moved = any(self.move(col) for col in cols)
        if moved: self.new_num()

    def move_down(self):
        cols = [BackGround.block_pos[i::-4][::-1] for i in range(3, -1, -1)]
        moved = any(self.move(col) for col in cols)
        if moved: self.new_num()

    def move_left(self):
        rows = [BackGround.block_pos[i * 4:(i + 1) * 4] for i in range(4)]
        moved = any(self.move(row) for row in rows)
        if moved: self.new_num()

    def move_right(self):
        rows = [BackGround.block_pos[i * 4:(i + 1) * 4][::-1] for i in range(4)]
        moved = any(self.move(row) for row in rows)
        if moved: self.new_num()

    def restart(self):
        self.score = 0
        self.is_win = True
        for block in self.block_turtle_dict.values():
            block.num = 0
            block.clear()
        self.background.turtle_show_text.clear()
        self.background.text_is_clear = True
        self.new_num()


if __name__ == '__main__':
    screen = turtle.Screen()
    screen.setup(430, 530)
    screen.bgcolor("#faf8ef")
    screen.title("2048")
    screen.tracer(0)

    game = Game()

    screen.listen()
    screen.onkey(game.move_up, "Up")
    screen.onkey(game.move_down, "Down")
    screen.onkey(game.move_left, "Left")
    screen.onkey(game.move_right, "Right")
    screen.onkey(game.restart, "space")

    while True:
        screen.update()