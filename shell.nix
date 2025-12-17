let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (
      python-pkgs: with python-pkgs; [
        # select Python packages here
        numpy
        matplotlib
        scipy
      ]
    ))
    pkgs.root
  ];

  # All'ingresso nel nix-shell, rimpiazza bash con fish
  shellHook = ''
    # Se NON siamo già in fish, passa a fish
    if [ -z "$FISH_VERSION" ]; then
      exec ${pkgs.fish}/bin/fish -l
    fi
  '';
}
