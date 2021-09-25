from setuptools import setup, find_packages

setup(
    name='youtube_crawler',
    version='1.0',
    description="crawling Yotube video's url, title, full description, caption, comment",
    author='Moon Ye Wan',
    author_email='mool1997@naver.com',
    url='https://github.com/Mo0nl19ht/youtube_crawler',
    install_requires=['google-api-python-client',
                      'oauth2client', 'pytube' 'tqdm', 'pandas'],
    packages=find_packages(exclude=[]),
    keywords=['youtube', 'crawler', 'textdata'],
    python_requires='>=3',

)
