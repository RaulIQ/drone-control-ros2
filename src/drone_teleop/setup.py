from setuptools import find_packages, setup

package_name = 'drone_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='RaulIQ',
    maintainer_email='raulalimbekov@gmail.com',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
            'pyhamcrest',
        ],
    },
    entry_points={
        'console_scripts': [
            'flight_manager = drone_teleop.flight_manager:main',
            'teleop_node = drone_teleop.teleop_node:main',
        ],
    },
)
