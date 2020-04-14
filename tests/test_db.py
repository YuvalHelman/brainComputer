import pytest

from brainComputer.db import get_db_handler


def insert_to_db(user_id, username):
    mong = get_db_handler('mongodb://127.0.0.1:27017')
    data = dict({'_id':user_id, 
'user': {'user_id':user_id, 'username': username, 'birthday': 699746400, 'gender': 0}, 
'snapshots': {'1575446887339': {
    'pose': {'translation': {'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985}, 
		'rotation': {'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748, 'w': 0.9571326384559261}},
	'color_image': {'width': 1920, 'height': 1080, 'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/color_data', 
						'color_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/color_image.png'}, 'depth_image': {'width': 224, 'height': 172, 'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/depth_data',
					'depth_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/depth_image.png'}, 
	'feelings': {'hunger': 0.0, 'thirst': 0.0, 'exhaustion': 0.0, 'happiness': 0.0}}}}
    ) 

    mong.insert_doc(data)


if __name__ == '__main__':
    insert_to_db(44, 'Yael Livne')

