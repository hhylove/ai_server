from setuptools import setup, find_packages

setup(
    name="ai_services",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "fastapi>=0.68.0",
        "python-multipart>=0.0.5",
        "typing-extensions>=4.0.0",
    ],
    author="hhy",
    author_email="505461850@qq.com",
    description="A library for AI services including ComfyUI and Coze",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hhylove/ai_server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.8",
) 