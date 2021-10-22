import pygame
import Utils
from my_image import *
from math import pow
from Grid import *
from queue import Queue
import sys
from tkinter import *
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import filedialog
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = str(500) + "," + str(150)  # controlling position of window where it appears

pygame.init()
screen = pygame.display.set_mode((Utils.SCREEN_SIZE_WIDTH, Utils.SCREEN_SIZE_HEIGHT))  # initializing screen size
pygame.display.set_caption("Paint")

icon = pygame.image.load('paint_icon.png')
pygame.display.set_icon(icon)


running = True
mouseButtonPressed = False


screen.fill(Utils.COLOR_WHITE)
util = Utils.Util()
util.selected_color = Utils.COLOR_BLACK


# This return the top left edge of every grid,  all calculations are done with respect to that grid
def get_grid_position(mx, my):
    if mx % util.stroke_length == 0 and my % util.stroke_length == 0:
        return mx, my
    elif mx % util.stroke_length != 0 and my % util.stroke_length == 0:
        return mx - (mx % util.stroke_length), my
    elif mx % util.stroke_length == 0 and my % util.stroke_length != 0:
        return mx, my - (my % util.stroke_length)
    else:
        return mx - (mx % util.stroke_length), my - (my % util.stroke_length)


#  Getting the respective grid index with the position of mx and my
def get_grid_index(mx, my):
    index_row = int(mx / 5)
    index_column = int(my / 5)
    return index_row, index_column


#  updating the original grid colors, only comes here for brush and eraser, not fill
def update_grid_position(mx, my):
    global grid
    index_row, index_column = get_grid_index(mx, my)
    replace_color = COLOR_WHITE
    if tools_eraser.toggle:
        pass
    else:
        replace_color = util.selected_color

    if util.stroke_length is 5:
        grid[index_row][index_column].color = replace_color
    elif util.stroke_length is 10:
        grid[index_row][index_column].color = replace_color
        grid[index_row + 1][index_column].color = replace_color
        grid[index_row][index_column + 1].color = replace_color
        grid[index_row + 1][index_column + 1].color = replace_color
    elif util.stroke_length is 15:
        grid[index_row][index_column].color = replace_color
        grid[index_row][index_column + 1].color = replace_color
        grid[index_row][index_column + 2].color = replace_color
        grid[index_row + 1][index_column].color = replace_color
        grid[index_row + 1][index_column + 1].color = replace_color
        grid[index_row + 1][index_column + 2].color = replace_color
        grid[index_row + 2][index_column].color = replace_color
        grid[index_row + 2][index_column + 1].color = replace_color
        grid[index_row + 2][index_column + 2].color = replace_color
    elif util.stroke_length is 20:
        grid[index_row][index_column].color = replace_color
        grid[index_row][index_column + 1].color = replace_color
        grid[index_row][index_column + 2].color = replace_color
        grid[index_row][index_column + 3].color = replace_color
        grid[index_row + 1][index_column].color = replace_color
        grid[index_row + 1][index_column + 1].color = replace_color
        grid[index_row + 1][index_column + 2].color = replace_color
        grid[index_row + 1][index_column + 3].color = replace_color
        grid[index_row + 2][index_column].color = replace_color
        grid[index_row + 2][index_column + 1].color = replace_color
        grid[index_row + 2][index_column + 2].color = replace_color
        grid[index_row + 2][index_column + 3].color = replace_color
        grid[index_row + 3][index_column].color = replace_color
        grid[index_row + 3][index_column + 1].color = replace_color
        grid[index_row + 3][index_column + 2].color = replace_color
        grid[index_row + 3][index_column + 3].color = replace_color


#  fill algorithm
def flood_fill(index_row, index_column, target_color, replacement_color):
    if target_color is replacement_color:
        return
    queue = Queue()
    queue.put((index_row, index_column))
    grid[index_row][index_column].color = replacement_color
    pygame.draw.rect(screen, replacement_color,
                     [index_row * 5, index_column * 5, Utils.STROKE_LENGTH_EXTRA_SMALL,
                      Utils.STROKE_LENGTH_EXTRA_SMALL])

    while not queue.empty():

        index_row, index_column = queue.get()
        try:
            if grid[index_row+1][index_column].color is target_color:
                grid[index_row+1][index_column].color = replacement_color
                pygame.draw.rect(screen, replacement_color,
                                 [(index_row+1) * 5, index_column * 5, Utils.STROKE_LENGTH_EXTRA_SMALL,
                                  Utils.STROKE_LENGTH_EXTRA_SMALL])
                queue.put((index_row+1, index_column))
        except IndexError as ex:
            pass

        try:
            if grid[index_row][index_column+1].color is target_color:
                grid[index_row][index_column+1].color = replacement_color
                pygame.draw.rect(screen, replacement_color,
                                 [index_row * 5, (index_column+1) * 5, Utils.STROKE_LENGTH_EXTRA_SMALL,
                                  Utils.STROKE_LENGTH_EXTRA_SMALL])
                queue.put((index_row, index_column+1))
        except IndexError as ex:
            pass

        try:
            if grid[index_row-1][index_column].color is target_color:
                grid[index_row-1][index_column].color = replacement_color
                pygame.draw.rect(screen, replacement_color,
                                 [(index_row - 1) * 5, index_column * 5, Utils.STROKE_LENGTH_EXTRA_SMALL,
                                  Utils.STROKE_LENGTH_EXTRA_SMALL])
                queue.put((index_row-1, index_column))
        except IndexError as ex:
            pass

        try:
            if grid[index_row][index_column-1].color is target_color:
                grid[index_row][index_column-1].color = replacement_color
                pygame.draw.rect(screen, replacement_color,
                                 [index_row * 5, (index_column-1) * 5, Utils.STROKE_LENGTH_EXTRA_SMALL,
                                  Utils.STROKE_LENGTH_EXTRA_SMALL])
                queue.put((index_row, index_column-1))
        except IndexError as ex:
            pass

       # pygame.display.update()
    # Flood Fill recursive
    # if index_row is 160 or index_column is 160:
    #     return
    # if grid[index_row][index_column].color is replacement_color:
    #     return
    # elif grid[index_row][index_column].color is not target_color:
    #     return
    # else:
    #
    #     pygame.draw.rect(screen, replacement_color,
    #                      [index_row * 5, index_column * 5, Utils.STROKE_LENGTH_EXTRA_SMALL,
    #                       Utils.STROKE_LENGTH_EXTRA_SMALL])
    #
    # flood_fill(index_row, index_column + 1, target_color, replacement_color)
    # flood_fill(index_row + 1, index_column, target_color, replacement_color)
    # flood_fill(index_row - 1, index_column, target_color, replacement_color)
    # flood_fill(index_row, index_column - 1, target_color, replacement_color)
    # return


# Eraser and brush actions here
def perform_tools_action(mx, my):

    if tools_brush.toggle:
        pygame.draw.rect(screen, util.selected_color,
                         [mx, my, util.stroke_length,
                          util.stroke_length])
    elif tools_eraser.toggle:
        pygame.draw.rect(screen, Utils.COLOR_WHITE,
                         [mx, my, util.stroke_length,
                          util.stroke_length])
    update_grid_position(mx, my)


# Stroke images in toolbar
def draw_strokes():
    if stroke_extra_small.toggle:
        screen.blit(stroke_extra_small.image_source_selected,
                    (stroke_extra_small.position_x, stroke_extra_small.position_y))
    else:
        screen.blit(stroke_extra_small.image_source, (stroke_extra_small.position_x, stroke_extra_small.position_y))

    if stroke_small.toggle:
        screen.blit(stroke_small.image_source_selected, (stroke_small.position_x, stroke_small.position_y))
    else:
        screen.blit(stroke_small.image_source, (stroke_small.position_x, stroke_small.position_y))

    if stroke_medium.toggle:
        screen.blit(stroke_medium.image_source_selected, (stroke_medium.position_x, stroke_medium.position_y))
    else:
        screen.blit(stroke_medium.image_source, (stroke_medium.position_x, stroke_medium.position_y))

    if stroke_large.toggle:
        screen.blit(stroke_large.image_source_selected, (stroke_large.position_x, stroke_large.position_y))
    else:
        screen.blit(stroke_large.image_source, (stroke_large.position_x, stroke_large.position_y))


def draw_files():

    screen.blit(open_image.image_source, (open_image.position_x, open_image.position_y))
    screen.blit(save_image.image_source, (save_image.position_x, save_image.position_y))


# Navigation tool bar
def draw_shapes():

    if shape_rectangle_filled.toggle:
        screen.blit(shape_rectangle_filled.image_source_selected,
                    (shape_rectangle_filled.position_x-2, shape_rectangle_filled.position_y-2))
    else:
        screen.blit(shape_rectangle_filled.image_source, (shape_rectangle_filled.position_x, shape_rectangle_filled.position_y))

    if shape_rectangle_unfilled.toggle:
        screen.blit(shape_rectangle_unfilled.image_source_selected,
                    (shape_rectangle_unfilled.position_x - 2, shape_rectangle_unfilled.position_y - 2))
    else:
        screen.blit(shape_rectangle_unfilled.image_source,
                    (shape_rectangle_unfilled.position_x, shape_rectangle_unfilled.position_y))


def draw_lines():
    if horizontal_line.toggle:
        screen.blit(horizontal_line.image_source_selected,
                    (horizontal_line.position_x, horizontal_line.position_y))
    else:
        screen.blit(horizontal_line.image_source, (horizontal_line.position_x, horizontal_line.position_y))

    if verical_line.toggle:
        screen.blit(verical_line.image_source_selected,
                    (verical_line.position_x, verical_line.position_y))
    else:
        screen.blit(verical_line.image_source, (verical_line.position_x, verical_line.position_y))

    if primary_diagonal_line.toggle:
        screen.blit(primary_diagonal_line.image_source_selected,
                    (primary_diagonal_line.position_x, primary_diagonal_line.position_y))
    else:
        screen.blit(primary_diagonal_line.image_source, (primary_diagonal_line.position_x, primary_diagonal_line.position_y))

    if secondary_diagonal_line.toggle:
        screen.blit(secondary_diagonal_line.image_source_selected,
                    (secondary_diagonal_line.position_x, secondary_diagonal_line.position_y))
    else:
        screen.blit(secondary_diagonal_line.image_source, (secondary_diagonal_line.position_x, secondary_diagonal_line.position_y))


# Tools Images in toolbar
def draw_tools():
    if tools_brush.toggle:
        screen.blit(tools_brush.image_source_selected, (tools_brush.position_x-3, tools_brush.position_y-3))
    else:
        screen.blit(tools_brush.image_source, (tools_brush.position_x, tools_brush.position_y))

    if tools_eraser.toggle:
        screen.blit(tools_eraser.image_source_selected, (tools_eraser.position_x-3, tools_eraser.position_y-3))
    else:
        screen.blit(tools_eraser.image_source, (tools_eraser.position_x, tools_eraser.position_y))

    screen.blit(tools_clear.image_source, (tools_clear.position_x, tools_clear.position_y))

    if tools_fill.toggle:
        screen.blit(tools_fill.image_source_selected, (tools_fill.position_x-3.5, tools_fill.position_y-3))
    else:
        screen.blit(tools_fill.image_source, (tools_fill.position_x, tools_fill.position_y))


def navigation_toolbar_draw():
    screen.blit(navigation_toolbar, (Utils.SCREEN_SIZE_WIDTH - 100, 0))
    draw_strokes()
    draw_tools()
    draw_files()
    draw_shapes()
    draw_lines()

    pygame.draw.rect(screen, util.selected_color,  # color selection display box
                     [843.5, 775, 15, 14])


# Euclidean distance between 2 points
def measure_distance(first_x, first_y, second_x, second_y):
    return pow((first_x - second_x) * (first_x - second_x) + (first_y - second_y) * (first_y - second_y), 0.5)


# Changing stroke
def change_stroke(mx, my):
    global shape_coordinate_one, shape_coordinate_two, shape_input_counter
    if measure_distance(mx, my, stroke_extra_small.position_x + 3.5, stroke_extra_small.position_y + 3.5) < 8:
        stroke_extra_small.toggle = True
        stroke_small.toggle = False
        stroke_medium.toggle = False
        stroke_large.toggle = False
        util.stroke_length = Utils.STROKE_LENGTH_EXTRA_SMALL
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0

    if measure_distance(mx, my, stroke_small.position_x + 5, stroke_small.position_y + 5) < 11:
        stroke_extra_small.toggle = False
        stroke_small.toggle = True
        stroke_medium.toggle = False
        stroke_large.toggle = False
        util.stroke_length = Utils.STROKE_LENGTH_SMALL
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0

    if measure_distance(mx, my, stroke_medium.position_x + 7.5, stroke_medium.position_y + 7.5) < 15:
        stroke_extra_small.toggle = False
        stroke_small.toggle = False
        stroke_medium.toggle = True
        stroke_large.toggle = False
        util.stroke_length = Utils.STROKE_LENGTH_MEDIUM
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0

    if measure_distance(mx, my, stroke_large.position_x + 10, stroke_large.position_y + 10) < 20:
        stroke_extra_small.toggle = False
        stroke_small.toggle = False
        stroke_medium.toggle = False
        stroke_large.toggle = True
        util.stroke_length = Utils.STROKE_LENGTH_LARGE
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0


# Changing tools
def change_tool(mx, my):
    global shape_coordinate_one, shape_coordinate_two, shape_input_counter
    if measure_distance(mx, my, tools_brush.position_x + IMAGE_MIDPOINT, tools_brush.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        tools_brush.toggle = True
        tools_eraser.toggle = False
        tools_fill.toggle = False
        shape_rectangle_unfilled.toggle = False
        shape_rectangle_filled.toggle = False
        verical_line.toggle = False
        horizontal_line.toggle = False
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0

    if measure_distance(mx, my, tools_eraser.position_x + IMAGE_MIDPOINT, tools_eraser.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        tools_brush.toggle = False
        tools_eraser.toggle = True
        tools_fill.toggle = False
        shape_rectangle_unfilled.toggle = False
        shape_rectangle_filled.toggle = False
        verical_line.toggle = False
        horizontal_line.toggle = False
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0
    if measure_distance(mx, my, tools_clear.position_x + IMAGE_MIDPOINT, tools_clear.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        pygame.draw.rect(screen, Utils.COLOR_WHITE, [0, 0, Utils.SCREEN_SIZE_WIDTH - 100, Utils.SCREEN_SIZE_HEIGHT])
        for i in range(NUMBER_OF_GRID_ROWS):
            for j in range(NUMBER_OF_GRID_COLUMNS):
                grid[i][j].color = Utils.COLOR_WHITE
        # reinitializing grid again

    if measure_distance(mx, my, tools_fill.position_x + IMAGE_MIDPOINT, tools_fill.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        tools_brush.toggle = False
        tools_eraser.toggle = False
        tools_fill.toggle = True
        shape_rectangle_unfilled.toggle = False
        shape_rectangle_filled.toggle = False
        verical_line.toggle = False
        horizontal_line.toggle = False
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0


def change_color(mx, my):
    color = screen.get_at((mx, my))[:3]
    if color == (158, 157, 158):
        return
    util.selected_color = color


def change_shape(mx, my):
    global shape_coordinate_one, shape_coordinate_two, shape_input_counter
    if measure_distance(mx, my, shape_rectangle_filled.position_x + IMAGE_MIDPOINT,
                        shape_rectangle_filled.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        shape_rectangle_filled.toggle = True
        tools_eraser.toggle = False
        tools_fill.toggle = False
        tools_brush.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = False
        verical_line.toggle = False
        horizontal_line.toggle = False
        shape_rectangle_unfilled.toggle = False

    if measure_distance(mx, my, shape_rectangle_unfilled.position_x + IMAGE_MIDPOINT,
                        shape_rectangle_unfilled.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        shape_rectangle_filled.toggle = False
        shape_rectangle_unfilled.toggle = True
        tools_eraser.toggle = False
        tools_fill.toggle = False
        tools_brush.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = False
        verical_line.toggle = False
        horizontal_line.toggle = False


def change_line(mx, my):
    global shape_coordinate_one, shape_coordinate_two, shape_input_counter
    if measure_distance(mx, my, horizontal_line.position_x + IMAGE_MIDPOINT_TWO,
                        horizontal_line.position_y + IMAGE_MIDPOINT_TWO) < IMAGE_CLICK_RANGE_TWO:
        tools_brush.toggle = False
        tools_eraser.toggle = False
        tools_fill.toggle = False
        shape_rectangle_filled.toggle = False
        horizontal_line.toggle = True
        verical_line.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = False
        shape_rectangle_unfilled.toggle = False

    if measure_distance(mx, my, verical_line.position_x + IMAGE_MIDPOINT_TWO,
                        verical_line.position_y + IMAGE_MIDPOINT_TWO) < IMAGE_CLICK_RANGE_TWO:
        tools_brush.toggle = False
        tools_eraser.toggle = False
        tools_fill.toggle = False
        shape_rectangle_filled.toggle = False
        horizontal_line.toggle = False
        verical_line.toggle = True
        shape_rectangle_unfilled.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = False

    if measure_distance(mx, my, primary_diagonal_line.position_x + IMAGE_MIDPOINT_TWO,
                        primary_diagonal_line.position_y + IMAGE_MIDPOINT_TWO) < IMAGE_CLICK_RANGE_TWO:
        tools_brush.toggle = False
        tools_eraser.toggle = False
        tools_fill.toggle = False
        shape_rectangle_filled.toggle = False
        horizontal_line.toggle = False
        verical_line.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0
        shape_rectangle_unfilled.toggle = False
        primary_diagonal_line.toggle = True
        secondary_diagonal_line.toggle = False

    if measure_distance(mx, my, secondary_diagonal_line.position_x + IMAGE_MIDPOINT_TWO,
                        secondary_diagonal_line.position_y + IMAGE_MIDPOINT_TWO) < IMAGE_CLICK_RANGE_TWO:
        tools_brush.toggle = False
        tools_eraser.toggle = False
        tools_fill.toggle = False
        shape_rectangle_filled.toggle = False
        horizontal_line.toggle = False
        shape_rectangle_unfilled.toggle = False
        verical_line.toggle = False
        shape_coordinate_one = None
        shape_coordinate_two = None
        shape_input_counter = 0
        primary_diagonal_line.toggle = False
        secondary_diagonal_line.toggle = True


def open_file():
    pygame.draw.rect(screen, Utils.COLOR_WHITE, [0, 0, Utils.SCREEN_SIZE_WIDTH-100, Utils.SCREEN_SIZE_HEIGHT])
    root = Tk()
    root.title('Codemy.com Image Viewer')

    root.filename = filedialog.askopenfilename(initialdir="saved images", title="Select an Image",
                                               filetypes=(("png Files", "*.png"), ("all Files", "*.*")))
    my_label = Label(root, text=root.filename).pack()
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label = Label(image=my_image).pack()
    #  print(root.filename)
    selected_image = pygame.image.load(root.filename)  # toolbar image
    screen.blit(selected_image, (0, 0))
    root.destroy()


def save_file():
    root = Tk()
    root.title('Codemy.com Image Viewer')
    files = [('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Document', '*.txt'),
             ('PNG File', '*.png')]
    file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
    # print(file)
    rect = pygame.Rect(0, 0, 800, 800)
    sub = screen.subsurface(rect)
    pygame.image.save(sub, file)
    root.destroy()


def files_action(mx, my):
    if measure_distance(mx, my, open_image.position_x + IMAGE_MIDPOINT, open_image.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        open_file()

    if measure_distance(mx, my, save_image.position_x + IMAGE_MIDPOINT, save_image.position_y + IMAGE_MIDPOINT) < IMAGE_CLICK_RANGE:
        save_file()


def fix_coordinates(shape_coordinate_one, shape_coordinate_two):
    one = measure_distance(0, 0, shape_coordinate_one[0], shape_coordinate_one[1])
    two = measure_distance(0, 0, shape_coordinate_two[0], shape_coordinate_two[1])
    if one <= two:
        return shape_coordinate_one, shape_coordinate_two
    else:
        return shape_coordinate_two, shape_coordinate_one


def draw_rectangle_filled(shape_coordinate_one, shape_coordinate_two):
    #  print("yoho")
    fix_coordinates(shape_coordinate_one, shape_coordinate_two)
    shape_coordinate_one = get_grid_position(shape_coordinate_one[0], shape_coordinate_one[1])
    shape_coordinate_two = get_grid_position(shape_coordinate_two[0], shape_coordinate_two[1])
    pygame.draw.rect(screen, util.selected_color, [shape_coordinate_one[0], shape_coordinate_one[1],
                                                  shape_coordinate_two[0]-shape_coordinate_one[0],
                                                  shape_coordinate_two[1]-shape_coordinate_one[1]])
    index_one = get_grid_index(shape_coordinate_one[0], shape_coordinate_one[1])
    index_two = get_grid_index(shape_coordinate_two[0], shape_coordinate_two[1])
    i = index_one[0]
    j = index_one[1]
    store_column = j
    while i < index_two[0]:
        j = store_column
        while j < index_two[1]:
            grid[i][j].color = util.selected_color
            j += 1
        i += 1


def draw_rectangle_unfilled(shape_coordinate_one, shape_coordinate_two):
    horizontal_line_draw(shape_coordinate_one, shape_coordinate_two)
    vertical_line_draw(shape_coordinate_one, shape_coordinate_two)
    horizontal_line_draw((shape_coordinate_one[0], shape_coordinate_two[1]), shape_coordinate_two)
    vertical_line_draw((shape_coordinate_two[0], shape_coordinate_one[1]), shape_coordinate_two)
    shape_coordinate_one = get_grid_position(shape_coordinate_one[0], shape_coordinate_one[1])
    shape_coordinate_two = get_grid_position(shape_coordinate_two[0], shape_coordinate_two[1])
    i, j = get_grid_index(shape_coordinate_two[0], shape_coordinate_two[1])
    update_grid_at_position(i,j)
    pygame.draw.rect(screen, util.selected_color,
                     [shape_coordinate_two[0], shape_coordinate_two[1], util.stroke_length, util.stroke_length])



def horizontal_line_draw(shape_coordinate_one, shape_coordinate_two):
    shape_coordinate_one = get_grid_position(shape_coordinate_one[0], shape_coordinate_one[1])
    shape_coordinate_two = get_grid_position(shape_coordinate_two[0], shape_coordinate_two[1])
    pygame.draw.rect(screen, util.selected_color, [shape_coordinate_one[0], shape_coordinate_one[1],
                                                   shape_coordinate_two[0] - shape_coordinate_one[0],
                                                   util.stroke_length])
    index_one = get_grid_index(shape_coordinate_one[0], shape_coordinate_one[1])
    index_two = get_grid_index(shape_coordinate_two[0], shape_coordinate_two[1])
    i = index_one[0]
    while i < index_two[0]:
        x = 0
        j = index_one[1]
        while x < util.stroke_length / 5:
            grid[i][j].color = util.selected_color
            j += 1
            x += 1
        i += 1


def vertical_line_draw(shape_coordinate_one, shape_coordinate_two):
    shape_coordinate_one = get_grid_position(shape_coordinate_one[0], shape_coordinate_one[1])
    shape_coordinate_two = get_grid_position(shape_coordinate_two[0], shape_coordinate_two[1])
    pygame.draw.rect(screen, util.selected_color, [shape_coordinate_one[0], shape_coordinate_one[1],
                                                   util.stroke_length,
                                                   shape_coordinate_two[1] - shape_coordinate_one[1]])
    index_one = get_grid_index(shape_coordinate_one[0], shape_coordinate_one[1])
    index_two = get_grid_index(shape_coordinate_two[0], shape_coordinate_two[1])
    i = index_one[1]
    while i < index_two[1]:
        x = 0
        j = index_one[0]
        try:
            while x < util.stroke_length / 5:
                grid[j][i].color = util.selected_color
                j += 1
                x += 1
            i += 1
        except IndexError as ex:
            pass

def update_grid_at_position(index_row, index_column):
    global grid
    replace_color = util.selected_color
    if util.stroke_length is 5:
        grid[index_row][index_column].color = replace_color
    elif util.stroke_length is 10:
        grid[index_row][index_column].color = replace_color
        grid[index_row + 1][index_column].color = replace_color
        grid[index_row][index_column + 1].color = replace_color
        grid[index_row + 1][index_column + 1].color = replace_color
    elif util.stroke_length is 15:
        grid[index_row][index_column].color = replace_color
        grid[index_row][index_column + 1].color = replace_color
        grid[index_row][index_column + 2].color = replace_color
        grid[index_row + 1][index_column].color = replace_color
        grid[index_row + 1][index_column + 1].color = replace_color
        grid[index_row + 1][index_column + 2].color = replace_color
        grid[index_row + 2][index_column].color = replace_color
        grid[index_row + 2][index_column + 1].color = replace_color
        grid[index_row + 2][index_column + 2].color = replace_color
    elif util.stroke_length is 20:
        grid[index_row][index_column].color = replace_color
        grid[index_row][index_column + 1].color = replace_color
        grid[index_row][index_column + 2].color = replace_color
        grid[index_row][index_column + 3].color = replace_color
        grid[index_row + 1][index_column].color = replace_color
        grid[index_row + 1][index_column + 1].color = replace_color
        grid[index_row + 1][index_column + 2].color = replace_color
        grid[index_row + 1][index_column + 3].color = replace_color
        grid[index_row + 2][index_column].color = replace_color
        grid[index_row + 2][index_column + 1].color = replace_color
        grid[index_row + 2][index_column + 2].color = replace_color
        grid[index_row + 2][index_column + 3].color = replace_color
        grid[index_row + 3][index_column].color = replace_color
        grid[index_row + 3][index_column + 1].color = replace_color
        grid[index_row + 3][index_column + 2].color = replace_color
        grid[index_row + 3][index_column + 3].color = replace_color


def primary_diagonal_line_draw(shape_coordinate_one, shape_coordinate_two):
    shape_coordinate_one = get_grid_position(shape_coordinate_one[0], shape_coordinate_one[1])
    shape_coordinate_two = get_grid_position(shape_coordinate_two[0], shape_coordinate_two[1])
    fix_coordinates(shape_coordinate_one, shape_coordinate_two)
    i = shape_coordinate_one[0]
    j = shape_coordinate_one[1]
    while True:
        if i >= shape_coordinate_two[0] or j >= shape_coordinate_two[1]:
            break

        pygame.draw.rect(screen, util.selected_color,
                         [i, j, util.stroke_length,
                          util.stroke_length])
        x, y = get_grid_index(i, j)
        update_grid_at_position(x, y)
        i += util.stroke_length
        j += util.stroke_length


def secondary_diagonal_line_draw(shape_coordinate_one, shape_coordinate_two):
    shape_coordinate_one = get_grid_position(shape_coordinate_one[0], shape_coordinate_one[1])
    shape_coordinate_two = get_grid_position(shape_coordinate_two[0], shape_coordinate_two[1])
    if shape_coordinate_one[1] > shape_coordinate_two[1]:
        shape_coordinate_one, shape_coordinate_two = shape_coordinate_two, shape_coordinate_one
    i = shape_coordinate_one[0]
    j = shape_coordinate_one[1]
    while True:
        if i <= shape_coordinate_two[0] or j >= shape_coordinate_two[1]:
            break
        pygame.draw.rect(screen, util.selected_color,
                         [i, j, util.stroke_length,
                          util.stroke_length])
        x, y = get_grid_index(i, j)
        update_grid_at_position(x, y)
        i -= util.stroke_length
        j += util.stroke_length


def lines_action():
    global shape_coordinate_one, shape_coordinate_two, grid
    fix_coordinates(shape_coordinate_one, shape_coordinate_two)
    if verical_line.toggle:
        vertical_line_draw(shape_coordinate_one, shape_coordinate_two)
    elif horizontal_line.toggle:
        horizontal_line_draw(shape_coordinate_one, shape_coordinate_two)
    elif primary_diagonal_line.toggle:
        primary_diagonal_line_draw(shape_coordinate_one, shape_coordinate_two)
    elif secondary_diagonal_line.toggle:
        secondary_diagonal_line_draw(shape_coordinate_one, shape_coordinate_two)


def do_sth(mx, my):
    global grid
   # print(get_grid_position(mx, my))
   # print(grid[mx][my].color)


while running:

    navigation_toolbar_draw()

    for event in pygame.event.get():  # this will capture every event that occurs
        if event.type == pygame.QUIT:  # when the cross button of top right of the
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            mx, my = get_grid_position(mx, my)
            x, y = get_grid_index(mx, my)
            try:
               # print("color : ", grid[x][y].color)
                pass
            except:
                pass
           # print(shape_rectangle_filled.toggle)
            if tools_fill.toggle:
                if mx < Utils.SCREEN_SIZE_WIDTH-100:
                    flood_fill(x, y, grid[x][y].color, util.selected_color)
            elif shape_rectangle_filled.toggle:
                if shape_input_counter is 0:
                    shape_coordinate_one = mx, my
                    shape_input_counter = 1
                elif shape_input_counter is 1:
                    shape_coordinate_two = mx, my
                    shape_input_counter = 0
                    draw_rectangle_filled(shape_coordinate_one, shape_coordinate_two)
            elif horizontal_line.toggle or verical_line.toggle or primary_diagonal_line.toggle or secondary_diagonal_line.toggle:
                if mx < 800:
                    if shape_input_counter is 0:
                        shape_coordinate_one = pygame.mouse.get_pos()
                        shape_input_counter = 1
                    elif shape_input_counter is 1:
                        shape_coordinate_two = pygame.mouse.get_pos()
                        shape_input_counter = 0
                        lines_action()
            elif shape_rectangle_unfilled.toggle:
                if shape_input_counter is 0:
                    shape_coordinate_one = pygame.mouse.get_pos()
                    shape_input_counter = 1
                elif shape_input_counter is 1:
                    shape_coordinate_two = pygame.mouse.get_pos()
                    shape_input_counter = 0
                    draw_rectangle_unfilled(shape_coordinate_one, shape_coordinate_two)
            else:
                mouseButtonPressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseButtonPressed = False
            mx, my = pygame.mouse.get_pos()

            if mx >= Utils.SCREEN_SIZE_WIDTH - 100:
                shape_coordinate_one = None
                shape_coordinate_two = None
                shape_input_counter = 0
                if my <= 60:  # stroke range
                    change_stroke(mx, my)

                if 75 <= my <= 400:  # tool range
                    change_tool(mx, my)

                if 615 <= my <= Utils.SCREEN_SIZE_HEIGHT:
                    change_color(mx, my)

                if 535 <= my <= 615:
                    files_action(mx, my)

                if 400 <= my <= 465:
                    change_shape(mx, my)

                if 465 <= my <= 530:
                    change_line(mx, my)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pass


        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            mx, my = pygame.mouse.get_pos()
            mx, my = get_grid_position(mx, my)
            mx, my = get_grid_index(mx, my)
            do_sth(mx, my)

    if mouseButtonPressed:
        mx, my = pygame.mouse.get_pos()
        if mx < Utils.SCREEN_SIZE_WIDTH - 100:  # navigation tool bar check
            mx, my = get_grid_position(mx, my)
            perform_tools_action(mx, my)

    pygame.display.update()
