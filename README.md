# How to use this project?

## VisualStudio Code + Docker (Recommended)
The easiest way to use this project is by opening this repo with VSCode and Docker.

Go to Extension by pressing `ctrl+shift+x` and search for *Remote - Containers* `ms-vscode-remote.remote-containers`.
Install this extension.
In the bottom left, you can click to *reopen in container*

If you are asked for a Python interpreter, choose `python 3.8`.

*Please Note:* If you are on Linux and use the *flatpak* version of VSCode, you are probably not having `docker`.
See [visualstudio.com](https://code.visualstudio.com/docs/setup/setup-overview) for other installation methods.

## Ubuntu/Debian

In addition to Python 3 (3.8 recommended), you need `pip` for installing `requirements.txt`.
The following additional packages are necessary:

```sh
apt-get install ghostscript libmagick++-6.q16-dev swig
```

Since imagemagic does not allow to convert a pdf to a png, you need to adjust the `policy.xml` as follows:
```
# Debian fix for imagemagick
# https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion
sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml
```

# How to create attacks?

Each attack is located in a subfolder of the `shadow-attack` directory.
You will find three subdirectories:

1. hide
2. replace
3. hide-and-replace

Each folder has one or more variants of the respective attack class.

You can simply open the contained `*.ipynb` Jupyter notebook and follow the instructions contained therein.
Sometimes, VSCode does not show any content on the file.
Please close and reopen the file in this case.



# What is in the other directories?

## resources

This directory contains ressources that are required for the shadow attacks.
These include a pdf signing tools, a demo RSA key, malicious fonts, etc.
You must not modify these files.

## shadow-demo-exploits

This directory contains sample exploits generated with the scripts in `shadow-attacks`.

## shadow-detector

This script detects malicious pdf files.