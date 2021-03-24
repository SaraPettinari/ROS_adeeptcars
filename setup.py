from setuptools import setup

package_name = 'adeeptcar'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['adeeptcar/launch/adeept_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move = adeeptcar.move:setup', 'led = adeeptcar.led:setup', 'ultrasonic = adeeptcar.ultrasonic:setup', 'controller = adeeptcar.controller:setup', 'status = adeeptcar.status:setup'
        ],
    },
)
