import copy

def pose_flatten(pose_dict):
    res = dict()
    for main_key, sub_dict in pose_dict.items():
        for sub_key, sub_val in sub_dict.items():
            res.update({main_key + '.' + sub_key : sub_val})
    return res

def gui_image_dict_prepare(image_dict, name):
    res = copy.deepcopy(image_dict)
    res.pop('data_path')
    res.pop(name+ '_path')
    return res
