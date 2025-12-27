let
  pkgs = import <nixpkgs> {
    config = {
      allowUnfree = true;
    };
  };
in
pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages (
      python-pkgs: with python-pkgs; [
      	requests
        numpy
        matplotlib
        scipy
        lmfit
      ]
    ))
    (vscode-with-extensions.override {
      vscode = vscodium;
      vscodeExtensions = with vscode-extensions; [
        ms-python.python
        ms-python.debugpy
        ms-python.vscode-pylance
        ms-python.black-formatter
        github.github-vscode-theme
      ];
    })
  ];

  shellHook = ''
    if [ -z "$FISH_VERSION" ]; then
      exec ${pkgs.fish}/bin/fish -l
    fi
  '';
}

