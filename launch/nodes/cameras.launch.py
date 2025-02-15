from launch_ros.actions import Node
from launch_ros.actions import LaunchDescription
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('selk_i')
    params_path = os.path.join(pkg_share, 'parameters/camera_params.yaml')
    
    cam_1 = Node(
            package='gscam2',
            executable='gscam_main',
            name='gscam_publisher_cam1',
            namespace='selk-i', 
            parameters=[
                params_path
            ],
            remappings=[
                ('/image_raw', 'camera0/image_raw'),
                ('/camera_info', 'camera0/camera_info')
            ],
            output='screen'
        )
    
    cam_2 = Node(
            package='gscam2',
            executable='gscam_main',
            name='gscam_publisher_cam2',
            namespace='selk-i',
            parameters=[
                params_path
            ],
            remappings=[
                ('/image_raw', 'camera0/image_raw'),
                ('/camera_info', 'camera0/camera_info')
            ],
            output='screen'
        )
    
    return LaunchDescription([cam_1, cam_2])