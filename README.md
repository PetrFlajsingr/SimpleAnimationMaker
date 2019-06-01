# SimpleAnimationMaker
A simple module to create animations.

This is a practice project for builder pattern. The entire animation is created using builders.

TODOs: 
* gif output (only mp4 for now)
* support for images of different sizes

Images are drawn in the order they are passed into the `AnimationMaker`. Multiple queues and drawable objects can be created.

Usage:
```
image = cv2.imread(PATH_TO_IMAGE)
drawable = Drawable2D(image)

builder = TransformQueueActionBuilder(drawable)
queue = builder \
    .interpolate(10).scale(2, 'x')\ # interpolate scaling by the factor of 2 over 10 frames
    .begin_loop(10) \ # loop over next section 10 times
        .each(10).translate(1, 0) \ # do translation for 10 frames
        .each(10).translate(-1, 0) \ # do translation for 10 frames
        .begin_loop(90) \ # inner loop repeated 90 times
            .once().rotate(1, 'z') \ # rotate image by 1 degree
        .end_loop() \
    .end_loop() \
    .build()
    
white = np.zeros([100, 100, 4], dtype=np.uint8)
white.fill(255)
background = Drawable2D(white)
    
config = {
    'length': 600,
    'fps': 60
}
maker = AnimationMaker(DESTINATION, config, [queue], [background, obj])
maker.create_animation()
```
