from core.Client import *
from input.Mouse import move
import cv2

def get_menu_location():
    wi = Client()
    bgr = wi.get_canvas([4, 4, 765, 503])
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours is not None:
        max_a, found = [0, contours[0]], False
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            area = cv2.contourArea(c)
            if (cv2.contourArea(c) > 1500) and (w > 50):
                if area > max_a[0]:
                    max_a, found = [area, c], True
        if found:
            x, y, w, h = cv2.boundingRect(max_a[1])
            b = wi.bounds
            return [x + b[0], y + b[1], w, y + h, h]


def get_menu_lines():
    loc = get_menu_location()
    if loc is not None:
        x, y, w, h, hr = loc
        menu_num = int(np.floor(hr / 15))
        ii = 0
        menu_lines = np.zeros((menu_num, 4))
        for i in range(0, menu_num):
            yn = int(y + 15 * i)
            menu_lines[ii] = x, yn - 2, x + w, yn + 17
            ii += 1
        return menu_lines


def get_menu_text():
    final_text = None
    char_locs = np.arange(33, 127)
    char_values = np.array([chr(i) for i in range(127)])
    char_imgs = np.array([cv2.imread('fonts/menu/' + str(char_locs[i]) + '.bmp', 0) for i in range(94)])
    lines = get_menu_lines()
    ii = 0
    if lines is not None:
        final_text = ["" for i in range(len(lines))]
        for line in lines:
            img = ImageGrab.grab(bbox=line.tolist())
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            _, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

            img = thresh
            loop, txt_found = 0, 0
            text = np.zeros((1000, 3))
            for c in char_imgs:
                loop += 1
                if c is None:
                    continue
                template = c
                method = eval('cv2.TM_CCOEFF_NORMED')
                res = cv2.matchTemplate(img, template, method)

                loc = np.where(res >= 0.98)
                for pt in zip(*loc[::-1]):
                    text[txt_found] = [char_locs[loop - 1], pt[0], pt[1]]
                    txt_found += 1
            text = np.resize(text, (txt_found, 3))
            if len(text) == 0:
                break
            text = text[text[:, 1].argsort()]

            text_str = char_values[[i for i in text[0:txt_found, 0]]]
            text = ''.join(text_str)
            final_text[ii] = text
            ii += 1
    return final_text


def choose_option(option):
    b = Client().bounds
    lines = get_menu_lines()
    strs_list = get_menu_text()
    index = 0
    if strs_list is not None:
        for strs in strs_list:
            if option in strs:
                line = lines[index]
                loc = int(line[0] - b[0]), int(line[1] - b[1]), int(line[2] - b[0]), int(line[3] - b[1])
                move(box=loc, click_left=True, box_offset=5)
            index += 1

