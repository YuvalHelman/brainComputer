import copy
import shutil
import os

from brainComputer import ROOT_DIR


def pose_flatten(pose_dict):
    """ A function that flattens the 'pose' parsed data dict to a one dimensional dict, for better view inside the GUI.
    :param pose_dict: A python dict with the original data
    """
    res = dict()
    for main_key, sub_dict in pose_dict.items():
        for sub_key, sub_val in sub_dict.items():
            res.update({main_key + '.' + sub_key: sub_val})
    return res


def gui_image_dict_prepare(image_dict, name, user_id, username, datetime):
    """ A function that alters the original json of an image parsed data.
        Removes path members and points to an original image path inside the app's directory
    :param image_dict: A python dict with the original data
    :param name: the probe's name (color_image / depth_image)
    :param user_id: user id to point to
    :param username: user name to point to
    :param datetime: The ID of the snapshot for this current image data
    """
    res = copy.deepcopy(image_dict)
    old_img_path = image_dict[name + '_path']

    html_images_dir_path = ROOT_DIR + 'gui/app/static/'
    os.makedirs(html_images_dir_path, exist_ok=True)
    new_image_name = name + '_' + str(user_id) + '_' + username + '_' + str(datetime) + '.png'
    shutil.copy2(old_img_path, html_images_dir_path + new_image_name)

    res.pop('data_path')
    res.pop(name + '_path')
    return res, new_image_name
