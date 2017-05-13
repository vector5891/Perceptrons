{ pkgs ? import <nixpkgs> { }
}:

with pkgs;
let
  pyp = python27Packages;

  sknn = pyp.buildPythonPackage {
    name = "sknn";
    src = fetchgit {
      url = "https://github.com/aigamedev/scikit-neuralnetwork.git";
      rev = "b7fd0c089bd7c721c4d9cf9ca71eed74c6bafc5e";
      sha256 = "1s9kk1iqf2n8x6f7p3pprd22j6h27i32ypqgy6vsf58d6lp8vg73";
    };
    propagatedBuildInputs =
      (with pyp; [Lasagne scikitlearn]);
  };

  atari-py = pyp.buildPythonPackage {
    name = "atari-py";
    src = fetchgit {
      url = "https://github.com/openai/atari-py.git";
      rev = "d63ced3941f25d289eb49234898f58281183d4ea";
      sha256 = "0l00yzgbkvs4ln8nm3lcyzjgwkqcfpz4x5h8shnx2c99c277dy8h";
    };
    propagatedBuildInputs =
      [cmake zlib] ++
      (with pyp; [six numpy]);
  };

#  mujoco-py = pyp.buildPythonPackage {
#    name = "mujoco-py";
#    src = fetchgit {
#      url = "https://github.com/openai/mujoco-py.git";
#      rev = "6d56181677fcbf5d93fdc354c993d0d1e82efed3";
#      sha256 = "0xma9s37m07jl3kmjmkzkq5mmdavysnj8scm8sfx1s01r5il54gx";
#    };
#    propagatedBuildInputs =
#      (with pyp; [six numpy pyopengl]);
#  };

  gym = pyp.buildPythonPackage {
    name = "gym";
    src = fetchgit {
      url = "https://github.com/openai/gym.git";
      rev = "cde3b5e63b886ce3303f6d0d92e95560df0b887d";
      sha256 = "086plsf2xqyg2ig7daqmqsbphaf8xmq1yc4b1vh7b68by7wph6zs";
    };
    installFlags = [".[atari] .[box2d]"];
    propagatedBuildInputs =
      [atari-py] ++
      (with pyp; [pyopengl pyglet requests2 six box2d numpy]);
  };

  constraint = pyp.buildPythonPackage {
    name = "python-constraint";
    src = fetchgit {
      url = "https://github.com/python-constraint/python-constraint";
      rev = "4d04c2f724d5859f7310346e508138f3cd82541b";
      sha256 = "14ypwd771z9al69bj1z5jj7qgw88bvrf8xpmyqznbjvdwqk3y0d4";
      fetchSubmodules = true;
    };
  };

in
  pkgs.stdenv.mkDerivation rec{
    name = "openai";
    propagatedBuildInputs =
      [gym pyp.tensorflow python27Full sknn constraint pyp.hypothesis];
    phases = ["installPhase"];
    installPhase = ''
      mkdir -p $out/share/${name}
      echo ${lib.makeLibraryPath propagatedBuildInputs} > $out/share/${name}/buildInputs.txt
    '';
  }
