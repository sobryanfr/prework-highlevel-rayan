import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():
    desc_dir = get_package_share_directory('talebot27_description')
    loc_dir = get_package_share_directory('talebot27_localization')
    slam_dir = get_package_share_directory('talebot27_slam')
    nav_dir = get_package_share_directory('talebot27_navigation')

    xacro_file = os.path.join(desc_dir, 'urdf', 'robot.urdf.xacro')
    robot_desc = xacro.process_file(xacro_file).toxml()

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}]
    )

    mock_node = Node(package='talebot27_mock', executable='mock_hardware')

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        parameters=[os.path.join(loc_dir, 'config', 'ekf.yaml')]
    )

    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[os.path.join(slam_dir, 'config', 'slam_toolbox.yaml')]
    )

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')),
        launch_arguments={'params_file': os.path.join(nav_dir, 'config', 'nav2_params.yaml'), 'use_sim_time': 'false'}.items()
    )

    rviz_node = Node(package='rviz2', executable='rviz2')

    return LaunchDescription([rsp_node, mock_node, ekf_node, slam_node, nav2_launch, rviz_node])
