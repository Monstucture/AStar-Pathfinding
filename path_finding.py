# a-star algorithm
from queue import PriorityQueue


class State(object):
    def __init__(self, value, parent,
                 start=0,
                 goal=0):

        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0

        if parent:
            self.path = parent.path[:]  # Make the copy of parent path [:]
            self.path.append(value)
            self.start = parent.start  # start
            self.goal = parent.goal  # Goal
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def GetDistance(self):
        pass

    def CreateChildren(self):
        pass


class StateString(State):
    def __init__(self, value, parent,
                 start=0,
                 goal=0):

        super(StateString, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()

    def GetDistance(self):
        # check for reached goal
        if self.value == self.goal:
            return 0
        dist = 0
        for i in range(len(self.goal)):
            letter = self.goal[i]
            try:
                dist += abs(i - self.value.index(letter))
            except:
                dist += abs(i - self.value.find(letter))
        return dist

    def CreateChildren(self):
        if not self.children:
            for i in range(len(self.goal) - 1):
                val = self.value
                val = val[:i] + val[i + 1] + val[i] + val[i + 2:]
                child = StateString(val, self)
                self.children.append(child)


class AStarSolver:
    def __init__(self, start, goal):
        self.path = []  # store final solution
        self.visitedQueue = []  # stop visit children again
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def Solve(self):
        startState = StateString(self.start, 0,  # 0 means no parent passed in
                                 self.start,
                                 self.goal)

        count = 0
        self.priorityQueue.put((0, count, startState))
        # All the magic in below
        while not self.path and self.priorityQueue.qsize():
            closestChild = self.priorityQueue.get()[2]
            closestChild.CreateChildren()
            self.visitedQueue.append(closestChild.value)

            for child in closestChild.children:
                if child.value not in self.visitedQueue:
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))

        if not self.path:
            print("Goal of %s is not possible!" % self.goal)

        return self.path


# MAIN
if __name__ == "__main__":
    start1 = "pwedeepii"
    goal1 = "pewdiepie"
    print("Starting...")

    a = AStarSolver(start1, goal1)
    a.Solve()

    for i in range(len(a.path)):
        print("{0}) {1}".format(i, a.path[i]))
