# How to use this project?

## VisualStudio Code + Docker
The easiest way to use this project is by opening this repo with VSCode and Docker.
Go to Extension by pressing `ctrl+shift+x` and search for *Remote - Containers* `ms-vscode-remote.remote-containers`.
Install this extension.
In the bottom left, you can click to *reopen in container*

## NixOS user

```
nix-shell --pure
pip install -r requirements.txt
```

## Other Distros

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You mabe need the following tools: (see `default.nix`):
- `vscode`: IDE
- `swig`: dependency for endesive
- `openssl` + headers: dependency for endesive
- `imagemagick` + headers (`imagemagick-dev`) dependency for: python wand

# How to create Attacks?

## Hidden Attack (Image Variant)
- Open `play_shadow_hidden_attack.ipynb` in VSCode.
- Follow the instructions