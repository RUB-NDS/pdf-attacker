#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

# Update the VARIANT arg in devcontainer.json to pick a Python version: 3, 3.8, 3.7, 3.6
# To fully customize the contents of this image, use the following Dockerfile instead:
# https://github.com/microsoft/vscode-dev-containers/tree/v0.109.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
#
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Allow the vscode user to pip install globally w/o sudo
ENV PIP_TARGET=/usr/local/pip-global
ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
ENV PATH=${PIP_TARGET}/bin:${PATH}
RUN mkdir -p ${PIP_TARGET} \
    && chown vscode:root ${PIP_TARGET} \
    && export SNIPPET="if [ \"\$(stat -c '%U' ${PIP_TARGET})\" != \"vscode\" ]; then chown -R vscode:root ${PIP_TARGET}; fi" \
    && echo "$SNIPPET" | tee -a /root/.bashrc >> /home/vscode/.bashrc \
    && echo "$SNIPPET" | tee -a /root/.zshrc >> /home/vscode/.zshrc

# [Optional] Uncomment this section to install additional packages.
#
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
   && apt-get -y install --no-install-recommends ghostscript libmagick++-6.q16-dev swig pdftk \
   #
   # Clean up
   && apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/* \
   # Debian fix for imagemagick
   # https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion
   && sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml
ENV DEBIAN_FRONTEND=dialog
