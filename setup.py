from setuptools import setup, find_packages

setup(
    name='gpt_pptx_summarizer',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'python-pptx',
        'openai',
        'pytest',
        'pytest-asyncio',
    ],
    entry_points={
        'console_scripts': [
            'run_web_api=web_api.scripts.app:main',
            'run_explainer=explainer.scripts.main:main',
            'run_client=client.scripts.client:main',
        ],
    },
    author='Dor Shukrun',
    author_email='dorke88Gmail.com',
    description='A package for summarizing PPTX files using GPT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Scaleup-Excellenteam/final-exercise-DSH93',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
