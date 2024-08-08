import setuptools

setuptools.setup(
    name="streamlit-globalrefresh",
    version="1.0.0",
    author="Piyush Kumar",
    author_email="piyush.kumar.iaf@gmail.com",
    description="Global refresh with locks for streamlit",
    long_description="Global refresh with locks for streamlit",
    long_description_content_type="text/plain",
    url="https://github.com/piyushK52/streamlit_globalrefresh",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.75",
    ],
)
