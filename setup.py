from setuptools import find_packages, setup

VERSION = '0.0.1'
DESCRIPTION = 'Unofficial BingChat API'
LONG_DESCRIPTION = 'This package provides an API for BingChat. The API allows users to access BingChat from Python.'

setup(
    name='bingchatAPI',
    packages=find_packages(include=['BingChatAPI']),
    version=VERSION,
    author="DarkMatter-999",
    author_email="<darkmatter999official@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=["aioconsole",
                      "autopep8",
                      "certifi",
                      "charset-normalizer",
                      "idna",
                      "pycodestyle",
                      "python-dotenv",
                      "requests",
                      "tomli",
                      "urllib3",
                      "websockets",
                      "idna",],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ], keywords=[
        "chatgpt",
        "gpt4",
        "bingchat",
        "bing",
        "openai",
        "api",
        "python",
        "lachine learning",
        "natural language processing",
    ]
)
