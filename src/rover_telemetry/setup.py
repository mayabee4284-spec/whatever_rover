from setuptools import find_packages, setup

package_name = 'rover_telemetry'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shahjadee Ayesha Shahreen',
    maintainer_email='user@todo.todo',
    description='Rover Telemetry Package for Project Altair Phase 3',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'telemetry_publisher = rover_telemetry.telemetry_publisher:main',
            'telemetry_monitor = rover_telemetry.telemetry_monitor:main',
            'state_machine = rover_telemetry.state_machine:main',
            'turtle_menu = rover_telemetry.turtle_menu:main',
        ],
    },
)