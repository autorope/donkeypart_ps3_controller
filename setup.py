from setuptools import setup, find_packages

setup(name='donkeypart_ps3_controller',
      version='0.0',
      description='Donkey part to drive your car with a PS3 bluetooth controller.',
      long_description='none',
      long_description_content_type="text/markdown",
      url='https://github.com/autorope/donkeypart_ps3_controller',
      author='Tawm Kramer',
      license='MIT',
      install_requires=[],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='selfdriving cars donkeycar diyrobocars',
      packages=find_packages(exclude=(['tests', 'docs', 'site', 'env'])),
      )
