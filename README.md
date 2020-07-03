# How to use this project?

## VisualStudio Code + Docker
The easiest way to use this project is by opening this repo with VSCode and Docker.

Go to Extension by pressing `ctrl+shift+x` and search for *Remote - Containers* `ms-vscode-remote.remote-containers`.
Install this extension.
In the bottom left, you can click to *reopen in container*

If you are asked for a Python interpreter, choose `python 3.8`.

*Please Note:* If you are on Linux and use the *flatpak* version of VSCode, you are probably not having `docker`.
See [visualstudio.com](https://code.visualstudio.com/docs/setup/setup-overview) for other installation methods.

# How to create attacks?

Each attack is located in a subfolder of the `shadow_attack` directory.
You will find three subdirectories:

1. hide
2. replace
3. hide-and-replace

Each folder has one or more variants of the respective attack class.

You can simply open the contained `*.ipynb` Jupyter notebook and follow the instructions contained therein.
Sometimes, VSCode does not show any content on the file.
Please close and reopen the file in this case.

# What is in the other directories?

## pdf-detector

You can find a detector for shadow attacks in this directory

## lib / fonts / signer

These directories are used by the shadow attacks.