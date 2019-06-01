

class TransformAction:
    def __init__(self, frame_count, action):
        self.__frame_count = frame_count
        self.__frame_counter = frame_count
        self.__action = action

    def do_action(self):
        self.__action()
        self.__frame_counter -= 1
        return self.is_done()

    def is_done(self):
        return self.__frame_counter == 0

    def reset(self):
        self.__frame_counter = self.__frame_count


class CombinedTransfomAction:
    def __init__(self, frame_count, actions):
        self.__frame_count = frame_count
        self.__frame_counter = frame_count
        self.__actions = actions

    def do_action(self):
        for action in self.__actions:
            action()
        self.__frame_counter -= 1
        return self.is_done()

    def is_done(self):
        return self.__frame_counter == 0

    def reset(self):
        self.__frame_counter = self.__frame_count


class LoopTransformAction:
    def __init__(self, loop_count, queue):
        self.__loop_count = loop_count
        self.__loop_counter = loop_count
        self.__queue = queue

    def do_action(self):
        self.__queue.do_action()

        if self.__queue.is_done():
            self.__loop_counter -= 1
            self.__queue.reset()
        return self.is_done()

    def is_done(self):
        return self.__loop_counter == 0

    def reset(self):
        self.__queue.reset()
        self.__loop_counter = self.__loop_count


class TransformActionQueue:
    def __init__(self, actions):
        self.__actions = actions
        self.__action_index = 0

    def do_action(self):
        action = self.__actions[self.__action_index]
        action.do_action()

        if action.is_done():
            self.__action_index += 1
        return self.is_done()

    def is_done(self):
        return self.__action_index == len(self.__actions)

    def reset(self):
        self.__action_index = 0
        for action in self.__actions:
            action.reset()
