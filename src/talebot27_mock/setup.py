from setuptools import setup
package_name = 'talebot27_mock'
setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rayan Kessouri',
    maintainer_email='kessouri.a.rayan@gmail.com',
    entry_points={'console_scripts': ['mock_hardware = talebot27_mock.mock_hardware:main']},
)
