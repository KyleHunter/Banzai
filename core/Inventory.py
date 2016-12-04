import numpy as np
import misc.Misc as Misc


def get_inv_locs(box=False):
    cy = 224
    if not box:
        inv = np.zeros((28, 2))
    else:
        inv = np.zeros((28, 4))
    for i in range(0, 28):
        cx = 574 + ((i % 4) * 42)
        if i % 4 == 0:
            cy = int(224 + ((i / 4) * 36))
        if not box:
            inv[i] = cx, cy
        else:
            inv[i] = cx - 20, cy - 17, cx + 20, cy + 17
    return inv.astype(int)


def inv_point(slot, box=False):
    loc = get_inv_locs(box)[slot]
    return loc


def item_size(slot):
    box = inv_point(slot, True)
    return Misc.count_color((120, 255, 1), (120, 255, 1), box)


def item_count():
    count = 0
    for i in range(0, 28):
        if item_size(i) > 0:
            count += 1
    return count

