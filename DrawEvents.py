from Drawable2D import Drawable2D


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


class TimedTransformActionBuilder:
    def __init__(self, event_builder, frame_count):
        self.__event_builder = event_builder
        self.__frame_count = frame_count

    def rotate(self, angle, axis):
        drawable = self.__event_builder.drawable
        action = lambda drawable=drawable, angle=angle, axis=axis: drawable.rotate(angle, axis)
        self.__event_builder.events.append(TransformAction(self.__frame_count, action))
        return self.__event_builder

    def scale(self, scaling_factor, axis):
        drawable = self.__event_builder.drawable
        action = lambda drawable=drawable, scaling_factor=scaling_factor, axis=axis: drawable.scale(scaling_factor,
                                                                                                    axis)
        self.__event_builder.events.append(TransformAction(self.__frame_count, action))
        return self.__event_builder

    def translate(self, delta_x, delta_y):
        drawable = self.__event_builder.drawable
        action = lambda drawable=drawable, delta_x=delta_x, delta_y=delta_y: drawable.translate(delta_x, delta_y)
        self.__event_builder.events.append(TransformAction(self.__frame_count, action))
        return self.__event_builder


class InterpolatedTransformActionBuilder(TimedTransformActionBuilder):
    def __init__(self, event_builder, frame_count):
        super().__init__(event_builder, frame_count)
        self.__event_builder = event_builder
        self.__frame_count = frame_count

    def rotate(self, angle, axis):
        return super().rotate(angle / self.__frame_count, axis)

    def scale(self, scaling_factor, axis):
        scaling_factor = scaling_factor**(1 / self.__frame_count)
        return super().scale(scaling_factor, axis)

    def translate(self, delta_x, delta_y):
        return super().translate(delta_x / self.__frame_count, delta_y / self.__frame_count)


class TransformQueueActionBuilder:
    def __init__(self, drawable: Drawable2D):
        self.events = []
        self.drawable = drawable

    def begin_loop(self, loop_count):
        return LoopTransformActionBuilder(self, loop_count)

    def once(self):
        return TimedTransformActionBuilder(self, 1)

    def each(self, frame_count: int):
        return TimedTransformActionBuilder(self, frame_count)

    def interpolate(self, frame_count: int):
        return InterpolatedTransformActionBuilder(self, frame_count)

    def after(self, frame_count):
        action = lambda: None
        self.events.append(TransformAction(frame_count, action))
        return self

    def reset(self):
        drawable = self.drawable
        action = lambda drawable=drawable: drawable.reset_model_matrix()
        self.events.append(TransformAction(1, action))
        return self

    def build(self):
        return TransformActionQueue(self.events)


class LoopTransformActionBuilder(TransformQueueActionBuilder):
    def __init__(self, event_builder, loop_count):
        super().__init__(event_builder.drawable)
        self.__event_builder = event_builder
        self.__loop_count = loop_count

    def end_loop(self):
        queue = self.build()
        self.__event_builder.events.append(LoopTransformAction(self.__loop_count, queue))
        return self.__event_builder
