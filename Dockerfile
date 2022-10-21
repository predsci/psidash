FROM  --platform=linux/arm64/v8 continuumio/miniconda3:4.10.3

RUN conda install jupyter jupytext -c conda-forge
RUN conda install -c plotly jupyter-dash
RUN pip install dash-bootstrap-components

# RUN pip install git+https://github.com/predsci/psidash.git
COPY . /psidash
RUN pip install -e /psidash
WORKDIR /psidash