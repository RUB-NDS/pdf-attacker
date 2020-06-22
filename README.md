# How to use this project?

## NixOS user

```
nix-shell
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