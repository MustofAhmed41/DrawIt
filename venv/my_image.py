import pygame

class MyImageClass:

    def __init__(self, position_x, position_y, toggle, image_source, image_source_selected):
        self.position_x = position_x
        self.position_y = position_y
        self.toggle = toggle
        self.image_source = image_source
        self.image_source_selected = image_source_selected


# STROKES IMAGES
stroke_extra_small = MyImageClass(810, 52, True, pygame.image.load('rectangle_extra_small.png'),
                                  pygame.image.load('rectangle_extra_small_selected.png'))
stroke_small = MyImageClass(825, 50, False, pygame.image.load('rectangle_small.png'),
                            pygame.image.load('rectangle_small_selected.png'))
stroke_medium = MyImageClass(845, 47, False, pygame.image.load('rectangle_medium_small.png'),
                             pygame.image.load('rectangle_medium_selected.png'))
stroke_large = MyImageClass(870, 43, False, pygame.image.load('rectangle_large_small.png'),
                            pygame.image.load('rectangle_large_selected.png'))

# TOOLS IMAGES
tools_brush = MyImageClass(830, 115, True, pygame.image.load('brush.png'),
                           pygame.image.load('brush_selected.png'))
tools_eraser = MyImageClass(830, 185, False, pygame.image.load('eraser.png'),
                            pygame.image.load('eraser_selected.png'))
tools_clear = MyImageClass(830, 335, False, pygame.image.load('clear.png'),
                           pygame.image.load('clear_selected.png'))
tools_fill = MyImageClass(832, 260, False, pygame.image.load('fill.png'),
                          pygame.image.load('fill_selected.png'))


navigation_toolbar = pygame.image.load('navigation_bar.png')


save_image = MyImageClass(858, 559, True, pygame.image.load('save_icon.png'),
                          pygame.image.load('save_icon.png'))
open_image = MyImageClass(811, 559, True, pygame.image.load('open_icon.png'),
                          pygame.image.load('open_icon.png'))

shape_rectangle_filled = MyImageClass(813, 427, False, pygame.image.load('rectangle_filled.png'),
                                      pygame.image.load('rectangle_filled_selected.png'))
shape_rectangle_unfilled = MyImageClass(857, 429, False, pygame.image.load('rectangle_unfilled.png'),
                                      pygame.image.load('rectangle_unfilled_selected.png'))

horizontal_line = MyImageClass(810, 500, False, pygame.image.load('horizontal_line.png'),
                                      pygame.image.load('horizontal_line_selected.png'))
verical_line = MyImageClass(830, 500, False, pygame.image.load('vertical_line.png'),
                                      pygame.image.load('vertical_line_selected.png'))
primary_diagonal_line = MyImageClass(850, 500, False, pygame.image.load('primary_diagonal_line.png'),
                                      pygame.image.load('primary_diagonal_line_selected.png'))
secondary_diagonal_line = MyImageClass(875, 500, False, pygame.image.load('secondary_diagonal_line.png'),
                                      pygame.image.load('secondary_diagonal_line_selected.png'))


shape_coordinate_one = None
shape_coordinate_two = None
shape_input_counter = 0


IMAGE_MIDPOINT = 15
IMAGE_MIDPOINT_TWO = 4
IMAGE_CLICK_RANGE = 28
IMAGE_CLICK_RANGE_TWO = 9

