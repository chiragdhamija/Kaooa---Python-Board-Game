"""
Pygame provides us with the functionalities to create a game
"""

import math
import time
import sys
import pygame

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)
moves_for_kill = {
    0: [[8, 9], [6, 5]],
    1: [[9, 5], [7, 6]],
    2: [[5, 6], [8, 7]],
    3: [[6, 7], [9, 8]],
    4: [[5, 9], [7, 8]],
    5: [[4, 9], [2, 6]],
    6: [[0, 5], [3, 7]],
    7: [[1, 6], [4, 8]],
    8: [[0, 9], [2, 7]],
    9: [[1, 5], [3, 8]],
}

moves = {
    0: [5, 9],
    1: [5, 6],
    2: [6, 7],
    3: [7, 8],
    4: [8, 9],
    5: [0, 1, 6, 9],
    6: [1, 2, 5, 7],
    7: [2, 3, 6, 8],
    8: [3, 7, 4, 9],
    9: [0, 5, 8, 4],
}
vacant_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
VULTURE_POSITION = -1


def find_intersection(line_a, line_b):
    """
    This function find intersection point of two lines
    """
    x1, y1, x2, y2 = line_a
    x3, y3, x4, y4 = line_b

    # Calculate slopes of the lines
    slope1 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float("inf")
    slope2 = (y4 - y3) / (x4 - x3) if x4 - x3 != 0 else float("inf")

    # Check if the lines are parallel
    if slope1 == slope2:
        return None  # Lines are parallel, no intersection

    # Calculate intersection point
    x_intersect = (
        (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    y_intersect = (
        (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    return [x_intersect, y_intersect]


def find_mouse_click(mouse_ki_position, final_cor_of_star, radius):
    """
    This function tells whether mouse is clicked within circles or not
    """
    for i in range(0, 10):
        distance_bw_mouse_centre = math.sqrt(
            (mouse_ki_position[0] - final_cor_of_star[i][0]) ** 2
            + (mouse_ki_position[1] - final_cor_of_star[i][1]) ** 2
        )
        if distance_bw_mouse_centre <= radius:
            return i
    return -1


def check_v_move_is_possible(index_pointed):
    """
    This function tells whether vulture can move at a position if it is vacant
    """
    if VULTURE_POSITION == -1:
        return 1
    if index_pointed in moves[VULTURE_POSITION]:
        return 1
    else:
        return 0


def check_kill_possible(index_pointed):
    """
    This function tells whether Vulture can perform a kill or not
    """
    if VULTURE_POSITION == -1:
        return 1
    list_for_kills = moves_for_kill[VULTURE_POSITION]
    if index_pointed == (list_for_kills[0][0]):
        check_pos = list_for_kills[0][1]
        if vacant_list[check_pos] == 0:
            return 1
        else:
            return 0
    elif index_pointed == (list_for_kills[1][0]):
        check_pos = list_for_kills[1][1]
        if vacant_list[check_pos] == 0:
            return 1
        else:
            return 0
    else:
        return 0


def check_c_move_possible(crows_position, index_pointed):
    """
    This function checks wheter a crow move is valid or not
    """
    if index_pointed in moves[crows_position]:
        return 1
    else:
        return 0


def check_available_moves_for_vulture():
    """
    This function checks are there any available moves for vulture or not
    """
    if VULTURE_POSITION == -1:
        return 1
    full_list_of_vac_moves = moves[VULTURE_POSITION]
    for i in full_list_of_vac_moves:
        if vacant_list[i] == -1:
            return 1

    full_list_of_killer_moves = moves_for_kill[VULTURE_POSITION]
    for complex_list in full_list_of_killer_moves:
        if vacant_list[complex_list[0]] == -1 and vacant_list[complex_list[1]] == 0:
            return 1

    return 0


def display_board_game(
    final_corn_of_star,
    circ_radius,
    dis_surf,
    crow_s,
    crow_k,
    tur,
    res,
    inv_move,
    c_o_p,
):
    """
    This function helps to display the board game
    """
    dis_surf.fill(white)
    pygame.draw.line(dis_surf, black, final_corn_of_star[0], final_corn_of_star[2], 4)
    pygame.draw.line(dis_surf, black, final_corn_of_star[0], final_corn_of_star[3], 4)
    pygame.draw.line(dis_surf, black, final_corn_of_star[2], final_corn_of_star[4], 4)
    pygame.draw.line(dis_surf, black, final_corn_of_star[4], final_corn_of_star[1], 4)
    pygame.draw.line(dis_surf, black, final_corn_of_star[1], final_corn_of_star[3], 4)

    circ_radius = 25.0
    for i in range(0, 10):
        pygame.draw.circle(dis_surf, black, final_corn_of_star[i], circ_radius, 4)
    if VULTURE_POSITION != -1:
        pygame.draw.circle(
            dis_surf,
            red,
            final_corn_of_star[VULTURE_POSITION],
            circ_radius,
            4,
        )

    for i in range(0, 10):
        if vacant_list[i] == -1:
            pygame.draw.circle(
                dis_surf,
                black,
                final_corn_of_star[VULTURE_POSITION],
                circ_radius,
                4,
            )
        elif vacant_list[i] == 0:
            pygame.draw.circle(dis_surf, green, final_corn_of_star[i], circ_radius, 0)
        elif vacant_list[i] == 1:
            pygame.draw.circle(dis_surf, red, final_corn_of_star[i], circ_radius, 0)
    if crow_s != -1:
        pygame.draw.circle(
            dis_surf,
            blue,
            final_corn_of_star[crow_s],
            circ_radius,
            5,
        )

    pygame.draw.circle(dis_surf, red, [700, 200], circ_radius, 0)
    font = pygame.font.Font(None, 40)
    text_line_4 = font.render(": Vulture", True, black)
    text_rect_4 = text_line_4.get_rect(topleft=(740, 190))
    dis_surf.blit(text_line_4, text_rect_4)

    pygame.draw.circle(dis_surf, green, [700, 300], circ_radius, 0)
    text_line_5 = font.render(": Crows", True, black)
    text_rect_5 = text_line_4.get_rect(topleft=(740, 290))
    dis_surf.blit(text_line_5, text_rect_5)

    text_line_7 = font.render(f"Crows used till now : {c_o_p}", True, black)
    text_rect_7 = text_line_4.get_rect(topleft=(100, 100))
    dis_surf.blit(text_line_7, text_rect_7)

    text_line_1 = font.render(f"Crows captured : {crow_k}", True, black)
    text_rect_1 = text_line_1.get_rect(topleft=(100, 200))
    dis_surf.blit(text_line_1, text_rect_1)

    if inv_move == 1:

        text_line_6 = font.render("Invalid Move", True, red)
        text_rect_6 = text_line_1.get_rect(topleft=(800, 900))
        dis_surf.blit(text_line_6, text_rect_6)

    if tur == 22:
        text_line_2 = font.render("Vultures'Turn", True, blue)
    elif tur == 3:
        text_line_2 = font.render("Crow's Turn", True, blue)
    text_rect_2 = text_line_2.get_rect(topleft=(100, 900))
    dis_surf.blit(text_line_2, text_rect_2)

    if res == 1:
        text_line_3 = font.render("Vulture Won", True, green)
    elif res == 0:
        text_line_3 = font.render("Crows Won", True, green)
    elif res == -1:
        text_line_3 = font.render("Game in Progress", True, red)
    text_rect_3 = text_line_3.get_rect(topleft=(375, 800))
    dis_surf.blit(text_line_3, text_rect_3)
    pygame.display.update()
    if res != -1:
        time.sleep(3)


pygame.init()


X = 1000.0
Y = 1000.0

display_surface = pygame.display.set_mode((X, Y))


pygame.display.set_caption("Drawing")


display_surface.fill(white)

given_ver = [[151, 5], [296, 111], [241, 282], [61, 282], [5, 111]]

scaled_ver = []
for l in given_ver:
    XC = l[0] * 1.5
    YC = l[1] * 1.5
    new_list = [XC, YC]
    scaled_ver.append(new_list)

X_CENTROID = 0.0
Y_CENTROID = 0.0
for l in scaled_ver:
    X_CENTROID += l[0]
    Y_CENTROID += l[1]
X_CENTROID = X_CENTROID / 5
Y_CENTROID = Y_CENTROID / 5
centroid = [X_CENTROID, Y_CENTROID]

shift = [X / 2 - centroid[0], Y / 2 - centroid[1]]

final_corners_of_star = []
for l in scaled_ver:
    XC = l[0] + shift[0]
    YC = l[1] + shift[1]
    new_list = [XC, YC]
    final_corners_of_star.append(new_list)
# pygame.draw.polygon(display_surface, black,
# 					final_corners_of_star,5)

# print(final_corners_of_star)


line1 = (
    final_corners_of_star[0][0],
    final_corners_of_star[0][1],
    final_corners_of_star[2][0],
    final_corners_of_star[2][1],
)
line2 = (
    final_corners_of_star[0][0],
    final_corners_of_star[0][1],
    final_corners_of_star[3][0],
    final_corners_of_star[3][1],
)
line3 = (
    final_corners_of_star[1][0],
    final_corners_of_star[1][1],
    final_corners_of_star[4][0],
    final_corners_of_star[4][1],
)
line4 = (
    final_corners_of_star[1][0],
    final_corners_of_star[1][1],
    final_corners_of_star[3][0],
    final_corners_of_star[3][1],
)
line5 = (
    final_corners_of_star[2][0],
    final_corners_of_star[2][1],
    final_corners_of_star[4][0],
    final_corners_of_star[4][1],
)
final_corners_of_star.append(find_intersection(line1, line3))
final_corners_of_star.append(find_intersection(line4, line1))
final_corners_of_star.append(find_intersection(line5, line4))
final_corners_of_star.append(find_intersection(line2, line5))
final_corners_of_star.append(find_intersection(line3, line2))
CIRCLE_RADIUS = 25.0

RESULT = -1
CROWS_ORIGINAL_PLACED = 0
TURN = 3
CROW_KILLED = 0
CROW_SELECTED = -1
RUNNING = True
INVALID_MOVE = 0
# infinite loop
while RUNNING:
    if CROW_KILLED == 4:
        print("Vulture Wins")
        RESULT = 1
        INVALID_MOVE = 0
        RUNNING = False

    if check_available_moves_for_vulture() == 0:
        RESULT = 0
        print("Crows wins")
        INVALID_MOVE = 0
        RUNNING = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if TURN == 22:
                print("Vultures's Turn")
                IND = -1
                mouse_position = pygame.mouse.get_pos()
                IND = find_mouse_click(
                    mouse_position, final_corners_of_star, CIRCLE_RADIUS
                )

                if IND == -1:
                    print("Invalid Move")
                    INVALID_MOVE = 1
                else:

                    if CROWS_ORIGINAL_PLACED == 0:
                        VULTURE_POSITION = IND
                        vacant_list[IND] = 1
                        INVALID_MOVE = 0
                        TURN = 3

                    else:
                        if vacant_list[IND] == -1:

                            if check_v_move_is_possible(IND) == 1:
                                if VULTURE_POSITION != -1:
                                    vacant_list[VULTURE_POSITION] = -1
                                VULTURE_POSITION = IND
                                vacant_list[IND] = 1
                                TURN = 3
                                INVALID_MOVE = 0

                            elif check_kill_possible(IND) == 1:
                                killing_list = moves_for_kill[VULTURE_POSITION]
                                KILLED_CROW_POS = -1
                                if IND == killing_list[0][0]:
                                    KILLED_CROW_POS = killing_list[0][1]
                                elif IND == killing_list[1][0]:
                                    KILLED_CROW_POS = killing_list[1][1]
                                CROW_KILLED += 1
                                vacant_list[KILLED_CROW_POS] = -1
                                vacant_list[VULTURE_POSITION] = -1
                                VULTURE_POSITION = IND
                                vacant_list[VULTURE_POSITION] = 1
                                TURN = 3
                                INVALID_MOVE = 0
                            else:
                                print("Invalid Move")
                                INVALID_MOVE = 1
                        else:
                            print("Invalid Move")
                            INVALID_MOVE = 1

            elif TURN == 3:
                print("Crows turn")
                if CROWS_ORIGINAL_PLACED < 7:
                    IND = -1
                    mouse_position = pygame.mouse.get_pos()
                    IND = find_mouse_click(
                        mouse_position, final_corners_of_star, CIRCLE_RADIUS
                    )
                    if IND == -1:
                        print("Invalid Move")
                        INVALID_MOVE = 1
                    else:
                        if vacant_list[IND] == -1:
                            CROWS_ORIGINAL_PLACED += 1
                            vacant_list[IND] = 0
                            TURN = 22
                            INVALID_MOVE = 0
                        else:
                            print("Invalid Move")
                            INVALID_MOVE = 1
                else:
                    IND = -1
                    mouse_position = pygame.mouse.get_pos()
                    IND = find_mouse_click(
                        mouse_position, final_corners_of_star, CIRCLE_RADIUS
                    )
                    if IND == -1:
                        print("Invalid Move1")
                        INVALID_MOVE = 1
                    else:
                        if CROW_SELECTED == -1:
                            if vacant_list[IND] == 0:
                                CROW_SELECTED = IND
                                print("Crow has been selected")
                                INVALID_MOVE = 0
                            else:
                                print("Invalid Move")
                                INVALID_MOVE = 1
                        else:
                            if vacant_list[IND] != -1:
                                print("Invalid Move")
                                INVALID_MOVE = 1
                            else:
                                CHECKING = check_c_move_possible(CROW_SELECTED, IND)
                                if CHECKING == 1:
                                    vacant_list[CROW_SELECTED] = -1
                                    vacant_list[IND] = 0
                                    CROW_SELECTED = -1
                                    TURN = 22
                                    INVALID_MOVE = 0
                                else:
                                    print("Invalid Move")
                                    INVALID_MOVE = 1
    display_board_game(
        final_corners_of_star,
        CIRCLE_RADIUS,
        display_surface,
        CROW_SELECTED,
        CROW_KILLED,
        TURN,
        RESULT,
        INVALID_MOVE,
        CROWS_ORIGINAL_PLACED,
    )

sys.exit()
