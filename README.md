# 🤖 Talebot27 — Autonomous Navigation Stack (Eurobot 2027)

[![ROS 2](https://img.shields.io/badge/ROS_2-Jazzy_Jalisco-blue.svg)](https://docs.ros.org/en/jazzy/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04_LTS-orange.svg)](https://ubuntu.com/)
[![Maintainer](https://img.shields.io/badge/Maintainer-Rayan_Kessouri-green.svg)](mailto:kessouri.a.rayan@gmail.com)

Architecture logicielle sous **ROS 2 Jazzy** pour le robot autonome **Talebot27** (Eurobot 2027).

## Compilation & Lancement
```bash
cd ~/talebot27_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch talebot27_bringup bringup.launch.py
