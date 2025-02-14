{ pkgs, lib, config, inputs, ... }:

{
  env.GREET = "devenv";

  packages = [
    pkgs.git
    pkgs.ffmpeg
    pkgs.mediainfo
    pkgs.libmediainfo
    pkgs.unrar
  ];

  languages.python.enable = true;
  languages.python.venv.enable = true;
  languages.python.venv.requirements = requirements/requirements_dev.txt;

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo Welcome to GG-BOT Upload Assistant
  '';
  scripts.versions.exec = ''
    git --version
    python3 --version
    mediainfo --version
    ffmpeg -version
  '';

  enterShell = ''
    hello
    versions
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running unit tests"
    pytest -vv --show-capture=stdout --cov-report=html --cov-report=xml --junitxml=junit_report.xml --cov=./ tests/
  '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
