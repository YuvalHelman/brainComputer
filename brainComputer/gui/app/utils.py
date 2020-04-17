import copy
import shutil
import os

from brainComputer import ROOT_DIR


def pose_flatten(pose_dict):
    res = dict()
    for main_key, sub_dict in pose_dict.items():
        for sub_key, sub_val in sub_dict.items():
            res.update({main_key + '.' + sub_key : sub_val})
    return res

def gui_image_dict_prepare(image_dict, name, user_id, username, datetime):
    res = copy.deepcopy(image_dict)
    old_img_path = image_dict[name + '_path']

    # Makes the directories tree under the html gui path
    html_images_dir_path = get_gui_dir(ROOT_DIR + 'gui/app/templates/images/', user_id, username, datetime)
    os.makedirs(html_images_dir_path, exist_ok=True)
    shutil.copy2(old_img_path, html_images_dir_path)

    image_link = html_images_dir_path + name + '.png'

    res.pop('data_path')
    res.pop(name+ '_path')
    return res, image_link


def get_gui_dir(data_path, user_id, username, datetime):
        return str(data_path) + str(user_id) + "_" + str(username) + "/" + str(datetime) + '/'  # /42_Ron Dan/15423/

