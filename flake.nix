{
  description = "Chess queen domination solver";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            uv
            python3Packages.clingo
            python3Packages.cffi
          ];

          shellHook = ''
            echo "Queen domination solver dev environment"
            echo "Python: $(python3 --version)"
            echo "uv: $(uv --version)"
          '';
        };
      });
}
