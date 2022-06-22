import setuptools

setuptools.setup(
    name = "htseq_tools",
    author = "Kyle Hernandez",
    author_email = "kmhernan@uchicago.edu",
    version = 0.5,
    description = "htseq-count output tools",
    url = "https://github.com/NCI-GDC/htseq-tool",
    license = "Apache 2.0",
    packages = setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'htseq-tools = htseq_tools.__main__:main'
        ]
    },
    install_requires = [
      'numpy==1.22.0'
    ]
)

