with import <nixpkgs> { };
let
  my-python-packages = python-packages:
    with python-packages; [
      notebook
      scipy
    ];
  my-python = python37.withPackages my-python-packages;
in pkgs.mkShell {
  buildInputs = [ pkgs.python37Packages.pip my-python pkgs.swig ];
  shellHook = ''
    alias pip="PIP_PREFIX='$(pwd)/_build/pip_packages' \pip"
    export PYTHONPATH="$(pwd)/_build/pip_packages/lib/python3.7/site-packages:$PYTHONPATH" 
    unset SOURCE_DATE_EPOCH
  '';
}
