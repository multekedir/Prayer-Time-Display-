

# import library
import os
import stat
import sys
import time
import pygame

from athan_times import athan_times
from iqama_time import iqama_time

"""
This program use's the python athan time calculation from http://praytimes.org/.
After gating the data from the calculation and the iqama.txt it will display
final result onto the screen.

Author: Multezem Kedir
Date: 1/4/2017
Version: 2.0
"""

file_list = []  # a list of all images being shown
title = "Prayer Time Display"  # caption of the window...
wait_time = 1  # default time to wait between updates (in seconds)

window = None  # display
prayer_win = None
slide_win = None

bg_color = (0, 128, 0)  # green
text_color = (255, 255, 255)  # white
athan = athan_times()  # get athan time
iqama = iqama_time()  # get iqama time


def create_window():
    """
    creates window in full screen and minimized
    :return: (Width,Height)
    """

    # create window in a full screen
    global window
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)

    window.fill(bg_color)
    pygame.display.flip()

    # get resolution of screen
    width, height = pygame.display.get_surface().get_size()
    return width, height


def walktree(top, callback):
    """recursively descend the directory tree rooted at top, calling the
    callback function for each regular file. Taken from the module-stat
    example at: http://docs.python.org/lib/module-stat.html
    """
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[stat.ST_MODE]
        if stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif stat.S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)


def addtolist(file, extensions=['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
    """Add a file to a global list of image files."""
    global file_list  # ugh
    filename, ext = os.path.splitext(file)
    e = ext.lower()
    # Only add common image types to the list.
    if e in extensions:
        print('Adding to list: ', file)
        file_list.append(file)
    else:
        print('Skipping: ', file, ' (NOT a supported image)')


def display_athan(font_size, font_color, bg_color, x, y):
    """
    Display athan time onto screen from athan_time class.

    :param font_size:  size of font
    :param font_color: foreground color in rgn
    :param bg_color: back ground color
    :param x: x cordite on screen
    :param y: y cordite on screen
    :return: None
    """
    font = pygame.font.SysFont("monospace", font_size + 10, bold=True)
    title = font.render('        Athan', 1, font_color)
    window.blit(title, (x + 30, y))

    x_offset = 30

    font = pygame.font.SysFont("monospace", font_size, bold=True)

    prayer_font = font.render(('Fajr:   ' + athan.get_prayertime('fajr', '12h')), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 10))

    prayer_font = font.render(('Dhuhr   ' + athan.get_prayertime('dhuhr', '12h')), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 85))

    prayer_font = font.render(('Asr     ' + athan.get_prayertime('asr', '12h')), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 160))

    prayer_font = font.render(('Maghrib ' + athan.get_prayertime('maghrib', '12h')), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 230))

    prayer_font = font.render(('Isha    ' + athan.get_prayertime('isha', '12h')), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 305))

    prayer_font = font.render(('Juma    ' + iqama.get_iqama("jumah")), 1, font_color)
    window.blit(prayer_font, (x+300 + x_offset, y + font_size + 390))


def display_iqama(font_size, font_color, bg_color, x, y):
    """
    Display iqama time onto screen from athan_time class.

    :param font_size:  size of font
    :param font_color: foreground color in rgn
    :param bg_color: back ground color
    :param x: x cordite on screen
    :param y: y cordite on screen
    :return: None
    """
    font = pygame.font.SysFont("monospace", font_size + 10, bold=True)
    title = font.render('Iqama', 1, font_color)
    window.blit(title, (x + 50, y))
    x_offset = 30

    font = pygame.font.SysFont("monospace", font_size, bold=True)

    prayer_font = font.render((iqama.get_iqama("fajr")), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 20))

    prayer_font = font.render((iqama.get_iqama("dhuhr")), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 95))

    prayer_font = font.render((iqama.get_iqama("asr")), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 170))

    prayer_font = font.render((iqama.get_iqama("maghrib")), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 245))

    prayer_font = font.render((iqama.get_iqama("isha")), 1, font_color)
    window.blit(prayer_font, (x + x_offset, y + font_size + 320))


def displayTimeDate(fontSize, font_color, bg_color, x, y):
    """
    gets time and date from the libraries and display it

    :param fontSize: size of the font for time. date is ser to be 10 less
    :param font_color: font color for both time and date
    :param bg_color: background color for time and date
    :param x: 'x' location of time and date is set 25 to the left
    :param y: 'y' location of time and date
    :return: height
    """

    # ====================================set font==================================================
    Datefont = pygame.font.SysFont("monospace", fontSize, bold=True)
    Timefont = pygame.font.SysFont("monospace", fontSize, bold=True)

    # ======================================render time and date ===================================
    current_date = Datefont.render(str(time.strftime("%a %b %d,%Y ")), 1, font_color)
    current_time = Timefont.render(str(time.strftime("%I:%M:%p")), 1, font_color)
    time_remaining = Timefont.render((athan.get_timeremaining()), 1, (255, 0, 0))

    # ========================================= Display Time and date ==================================
    window.blit(current_date, (x, y))
    window.blit(current_time, (x + 200, y + 30 + fontSize))
    window.blit(time_remaining, (x - 150, y + 25 + (fontSize * 2)))


def runAll(p_w, s_w, h, startdir="."):
    """

    :param p_w:
    :param s_w:
    :param h:
    :param startdir:
    :return:
    """
    # ================================== set global variables========================================
    global file_list, title, wait_time, myfont

    # ====================================get img files to display====================================
    if not pygame.image.get_extended():
        print("Your Pygame isn't built with extended image support.")
        print("It's likely this isn't going to work.")
        sys.exit(1)
    walktree(startdir, addtolist)  # this may take a while...
    if len(file_list) == 0:
        print("Sorry. No images found. Exiting.")
        sys.exit(1)

    current = 0
    num_files = len(file_list)
    print(num_files)
    p_y = ((40 * 3) + h / 6) + 60
    # ========================================= run =================================================
    while True:
        try:
            slide = pygame.image.load(file_list[current]).convert()  # load img file
            slides = pygame.Rect(0, 0, s_w * 2, h)  # anchor slide to top right conner
            slide = pygame.transform.scale(slide, slides.size)  # make img fit to screen
            window.blit(slide, (0, 0))  # display img

            get_input(pygame.event.get())  # get input
            displayTimeDate(90, text_color, bg_color, 450, 50)  # display  time and date
            display_athan(90, text_color, bg_color, 160, p_y)  # display athan
            display_iqama(90, text_color, bg_color, p_w + 100, p_y )  # display iqama

            pygame.display.flip()  # update display
            time.sleep(wait_time)  # wait and run again

        except pygame.error as err:
            #  report any error
            print("Failed to display %s: %s" % (file_list[current], err))

        current = (current + 1) % num_files  # change the file to load


# ======================================================================================================

def get_input(events):
    """    setup input
    if ESC is hit quit program
    if f is hit resize image
    :param events: input data from pygame
    :return: None
    """
    for event in events:
        # Check if a key is pressed
        if event.type == pygame.KEYDOWN:
            # ESC key
            if event.key == pygame.K_ESCAPE:
                # quit program
                print("Closing Application")
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
		pygame.quit()
		os.system('../Scripts/runJava.sh')
                quit()
        elif event.type == pygame.QUIT:
            print("Closing Application")
            pygame.quit()
            quit()


def setup_window():
    '''
    arrange window
    :return: None
    '''
    w, h = create_window()

    p_window_width = w / 2
    s_window_width = w - p_window_width
    print('width= ' + str(p_window_width))
    runAll(p_window_width, s_window_width, h)


def main():
    """
    Run program
    :return: None
    """
    pygame.init()
    while True:
        setup_window()

main()
