import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression, EqualsSubstitution, IfElseSubstitution, OrSubstitution
from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = get_package_share_directory("selk_i")

    sim_mode = LaunchConfiguration("sim_mode")
    namespace = LaunchConfiguration("namespace")

    rsp_node = Node(
        name="robot_state_publisher",
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": PythonExpression(
                    [
                        "xacro.process_file('",
                        os.path.join(pkg_share, "urdf", "rov.urdf.xacro"),
                        "',mappings={'sim_mode':'",
                        EqualsSubstitution(sim_mode, 'true'), # Sanitize input
                        "'}).toxml()"
                    ],
                    ['xacro']
                ),
                "frame_prefix": IfElseSubstitution(OrSubstitution(EqualsSubstitution(namespace, "/"), EqualsSubstitution(namespace, "")), "", [namespace, "/"]),
            },
            os.path.join(pkg_share, "parameters", "robot_state_publisher.yaml"),
        ],
        namespace=namespace,
        remappings=[('/tf','tf'),('/tf_static','tf_static')], # Remap tf topics to the namespace
    )


    return LaunchDescription([
        DeclareLaunchArgument(
            "sim_mode",
            default_value="false",
            description="Set to true when running in a simulator"
        ),
        DeclareLaunchArgument(
            'namespace',
            default_value="/selk_i",
            description="Namespace of the bot (usually its unique identifier)"
        ),

        rsp_node
    ])
