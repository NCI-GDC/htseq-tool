import setuptools

setuptools.setup(
        name = "htseq-tool",
        author = "Stuti Agrawal",
        author_email = "stutia@uchicago.edu"
        version = 0.1,
        description = "rna-seq quantification tools",
        url = "https://github.com/NCI-GDC/htseq-tool",
        license = "Apache 2.0",
        packages = setuptools.find_packages(),
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            ],
    )

