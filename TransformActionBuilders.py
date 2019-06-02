from Drawable2D import Drawable2D
from TransformActions import TransformAction, CombinedTransfomAction, LoopTransformAction, TransformActionQueue


class TimedTransformActionBuilder:
    @property
    def parent(self):
        return self.__event_builder

    @property
    def frame_count(self):
        return self.__frame_count

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

    def combine_start(self):
        return CombinedTransformActionBuilder(self)


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

    def fade_out(self):
        drawable = self.__event_builder.drawable
        action = lambda drawable=drawable: drawable.add_to_alpha(-1 / self.__frame_count)
        self.__event_builder.events.append(TransformAction(self.__frame_count, action))
        return self.__event_builder

    def fade_in(self):
        drawable = self.__event_builder.drawable
        action = lambda drawable=drawable: drawable.add_to_alpha(1 / self.__frame_count)
        self.__event_builder.events.append(TransformAction(self.__frame_count, action))
        return self.__event_builder


class CombinedTransformActionBuilder:
    @property
    def parent(self):
        return self.__event_builder

    def __init__(self, event_builder):
        self.__event_builder = event_builder
        self.__actions = []

    def rotate(self, angle, axis):
        drawable = self.parent.parent.drawable
        action = lambda drawable=drawable, angle=angle, axis=axis: drawable.rotate(angle, axis)
        self.__actions.append(action)
        return self

    def scale(self, scaling_factor, axis):
        drawable = self.parent.parent.drawable
        action = lambda drawable=drawable, scaling_factor=scaling_factor, axis=axis: drawable.scale(scaling_factor,
                                                                                                    axis)
        self.__actions.append(action)
        return self

    def translate(self, delta_x, delta_y):
        drawable = self.parent.parent.drawable
        action = lambda drawable=drawable, delta_x=delta_x, delta_y=delta_y: drawable.translate(delta_x, delta_y)
        self.__actions.append(action)
        return self

    def combine_end(self):
        self.parent.parent.events.append(CombinedTransfomAction(self.parent.frame_count, self.__actions))
        return self.parent.parent


class TransformActionQueueBuilder:
    def __init__(self, drawable, converter=None):
        self.events = []
        self.drawable = drawable
        self.converter = converter

    def __convert_to_frames(self, value):
        if self.converter is not None:
            return self.converter.convert(value)
        return value

    def begin_loop(self, loop_count):
        return LoopTransformActionQueueBuilder(self, loop_count)

    def once(self):
        return TimedTransformActionBuilder(self, 1)

    def each(self, frame_count):
        return TimedTransformActionBuilder(self, self.__convert_to_frames(frame_count))

    def interpolate(self, frame_count):
        return InterpolatedTransformActionBuilder(self, self.__convert_to_frames(frame_count))

    def after(self, frame_count):
        action = lambda: None
        self.events.append(TransformAction(self.__convert_to_frames(frame_count), action))
        return self

    def reset(self):
        drawable = self.drawable
        action = lambda drawable=drawable: drawable.reset_model_matrix()
        self.events.append(TransformAction(1, action))
        return self

    def build(self):
        return TransformActionQueue(self.events)


class LoopTransformActionQueueBuilder(TransformActionQueueBuilder):
    @property
    def parent(self):
        return self.__event_builder

    def __init__(self, event_builder, loop_count):
        super().__init__(event_builder.drawable, event_builder.converter)
        self.__event_builder = event_builder
        self.__loop_count = loop_count

    def end_loop(self):
        queue = self.build()
        self.__event_builder.events.append(LoopTransformAction(self.__loop_count, queue))
        return self.__event_builder
