try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='send_email',
    version='201212',
    packages=[''],
    url='https://github.com/shuge/send_email',
    license='MIT License',
    author='Shuge Lee',
    author_email='shuge.lee@gmail.com',
    description='A simple send E-Mail script in pure Python',

    scripts = [
        "send_email.py",
    ],
)
