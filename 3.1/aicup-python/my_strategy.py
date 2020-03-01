import model
from math import floor, inf
from random import randrange


class MyStrategy:
    def __init__(self):
        pass

    def region(self, pos):
        x = floor(pos.x)
        y = floor(pos.y)
        # print(x, " ", y)
        Type = [self.game.level.tiles[x + 1][y], self.game.level.tiles[x - 1][y],
                self.game.level.tiles[x][y + 1], self.game.level.tiles[x][y - 1]]
        return Type

    def los(self, pos1, pos2, debug):
        if not (pos1.x < pos2.x or pos1.y < pos2.y):
            pos1, pos2 = pos1, pos2
        width = round(pos2.x - pos1.x)
        height = round(pos2.y - pos1.y)
        max_ = max(width, height)
        if max_ != 0:
            _height = height / max_
            _width = width / max_
            for i in range(max_):

                if self.game.level.tiles[round(pos1.x + i * _width)][round(pos1.y + i * _height)] == 1:
                    return False
            return True
        return True

    def RRT(self, start_pos, end_pos):
        self.tree = [Node(self.unit, None, self.game)]
        goal = [model.Vec2Double(floor(end_pos.x), floor(end_pos.y)), model.Vec2Double(floor(end_pos.x + 1), floor(
            end_pos.y)), model.Vec2Double(floor(end_pos.x), floor(end_pos.y + 1)), model.Vec2Double(floor(end_pos.x + 1), floor(end_pos.y + 1))]

        while len(self.tree) != 1000:
            xsamp = model.Vec2Double(randrange(1, 40), randrange(1, 30))

            dist = [comp(xsamp, n.pos) for n in self.tree]

            near = dist.index(min(dist))
            nearNode = self.tree[near]
            nearNode.pick(xsamp, self)

            leaf = model.Vec2Double(floor(self.tree[-1].pos.x), floor(self.tree[-1].pos.y))
            if leaf in goal:
                return self.tree[-1].set(self.debug)

    def get_action(self, unit, game, debug):
        # Replace this code with your own
        self.game = game
        self.unit = unit
        self.debug = debug

        def distance_sqr(a, b):
            return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
        nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, self.game.units),
            key=lambda u: distance_sqr(u.position, unit.position),
            default=None)
        nearest_weapon = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Weapon), self.game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)
        target_pos = nearest_enemy.position

        action = self.RRT(unit.position, nearest_weapon.position)

        aim = model.Vec2Double(0, 0)
        if nearest_enemy is not None:
            aim = model.Vec2Double(
                nearest_enemy.position.x - unit.position.x,
                nearest_enemy.position.y - unit.position.y)
        jump = target_pos.y > unit.position.y
        if target_pos.x > unit.position.x and self.game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        if target_pos.x < unit.position.x and self.game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True

        debug.draw(model.CustomData.Log(f"{action}"))
        if action != None:
            return model.UnitAction(
                velocity=action[0],
                jump=action[1],
                jump_down=action[2],
                aim=aim,
                shoot=False,
                reload=False,
                swap_weapon=False,
                plant_mine=False)
        else:
            return model.UnitAction(
                velocity=0,
                jump=False,
                jump_down=False,
                aim=aim,
                shoot=False,
                reload=False,
                swap_weapon=False,
                plant_mine=False)


class Node():
    def __init__(self, unit, parent, game):
        self.unit = unit
        self.pos = unit.position
        self.game = game
        self.jump_state = unit.jump_state
        self.parent = parent
        self.prop = self.game.properties
        self.stateX = [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9, 10, -10]
        self.stateY = [0, 1, -1]
        self.kids = []
        self.go = 0

    def get_cords(self, xstate, ystate):
        time = 1/(self.prop.ticks_per_second * self.prop.updates_per_tick)
        if ystate == 1:
            height = self.prop.unit_jump_speed / time
            if self.game.level.tiles[floor(self.pos.x)][floor(self.pos.y)] == 4:
                height = self.prop.jump_pad_jump_speed / time
        if ystate == -1:
            height = self.prop.unit_fall_speed / time
        if ystate == 0:
            height = 0

        width = self.prop.unit_max_horizontal_speed / (time)

        return model.Vec2Double(self.pos.x + width * xstate, self.pos.y + height * ystate)

    def set(self, debug):
        self.go = 1
        if self.parent != None:
            self.parent.set()
        else:
            return self.execute(debug)

    def execute(self, debug):
        for kid in self.kids:
            debug.draw(model.CustomData.Log(f"{kid.xstate} {kid.ystate}"))
            if kid.go == 1:
                debug.draw(model.CustomData.Log(f"Entered"))
                hvel = kid.xstate
                if kid.ystate == 0:
                    ujump = False
                    djump = False
                if kid.ystate == 1:
                    ujump = True
                    djump = False
                if kid.ystate == -1:
                    ujump = False
                    djump = True
                debug.draw(model.CustomData.Log(f"{hvel} {ujump} {djump}"))
                return hvel, ujump, djump

    def pick(self, xsamp, strat):
        self.debug = strat.debug
        min_ = inf
        for x in self.stateX:
            for y in self.stateY:
                if min_ > comp(xsamp, self.get_cords(x, y)):
                    min_ = comp(xsamp, self.get_cords(x, y))
                    xstate = x
                    ystate = y

        if strat.los(self.get_cords(xstate, ystate), self.pos, self.debug) == True:
            n = Node(self.unit, self, self.game)
            n.xstate = xstate
            n.ystate = ystate
            self.kids.append(n)
            strat.tree.append(n)


def comp(pos1, pos2):
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
