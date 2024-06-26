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
)
