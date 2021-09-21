from setuptools import setup, find_packages

setup(
    name='youtube_crawler',
    version='1.0',
    description="crawling Yotube video's url, title, full description, caption, comment",
    author='Moon Ye Wan',
    author_email='mool1997@naver.com',
    url='https://github.com/Mo0nl19ht/youtube_crawler',
    # download_url     = '',
    install_requires=[],
    packages=find_packages(exclude=['docs', 'tests*']),
    keywords=['youtube', 'crawler', 'textdata'],
    python_requires='>=3',
    package_data={
        'pyquibase': [
            'db-connectors/sqlite-jdbc-3.18.0.jar',
            'db-connectors/mysql-connector-java-5.1.42-bin.jar',
            'liquibase/liquibase.jar'
        ]},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
