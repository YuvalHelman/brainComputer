from pathlib import Path


def pbuser_to_dict(pb_user):
    return dict(
        user_id=pb_user.user_id,
        username=pb_user.username,
        birthday=pb_user.birthday,
        gender=pb_user.gender
    )


def pbsnapshot_to_dict(pb_snapshot, save_path):
    p = Path(save_path)
    color_data_p = p / 'color_data'
    with color_data_p.open() as f:
        f.write(pb_snapshot.color_image.data)

    depth_data_p = p / 'depth_data'
    with depth_data_p.open() as f:
        f.write(pb_snapshot.depth_image.data)

    return dict(
        datetime=pb_snapshot.datetime,
        pose=dict(
            translation=dict(
                x=pb_snapshot.pose.translation.x,
                y=pb_snapshot.pose.translation.y,
                z=pb_snapshot.pose.translation.z,
            ),
            rotation=dict(
                x=pb_snapshot.pose.rotation.x,
                y=pb_snapshot.pose.rotation.y,
                z=pb_snapshot.pose.rotation.z,
                w=pb_snapshot.pose.rotation.w,
            ),
        ),
        color_image=dict(
            width=pb_snapshot.color_image.width,
            height=pb_snapshot.color_image.height,
            data_path=str(color_data_p),
        ),
        depth_image=dict(
            width=pb_snapshot.depth_image.width,
            height=pb_snapshot.depth_image.height,
            data_path=str(depth_data_p),
        ),
        feelings=dict(
            hunger=pb_snapshot.feelings.hunger, thirst=pb_snapshot.feelings.thirst,
            exhaustion=pb_snapshot.feelings.exhaustion, happiness=pb_snapshot.feelings.happiness
        )
    )
