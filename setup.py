from setuptools import setup, find_packages

# Função para ler o requirements.txt
def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    name="estudante",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),  # Lê diretamente do arquivo requirements.txt
    entry_points={
        'console_scripts': [
            'estudante=estudante:main',
        ],
    },
    author="Pedro Duarte Blanco",
    author_email="pedblan@gmail.com",
    description="Transcreva suas aulas em vídeo ou áudio, não importa a duração. Encontre o ponto que deseja com um CTRL + F.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pedblan/estudante",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
)
