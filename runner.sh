#!/usr/bin/bash
# -------------------------------------------------------------------------
# Include external bash libs
# -------------------------------------------------------------------------

DEFAULT_BASH_LIB_DIR="${HOME}/bash-lib"
BASH_LIB_DIR=${BASH_LIB_DIR:-${DEFAULT_BASH_LIB_DIR}}
OUTPUT_HELPER_FILE="$BASH_LIB_DIR/output-helper.sh"
OUTPUT_HELPER_URL="https://gist.githubusercontent.com/jeremypruitt/6b1bcd6bcfbff1daa75624d9d12ac6e5/raw/9d51a75afd4fac32ca4215bd15ac7b0804661671/output-helper.sh"
BRIGHT=`tput bold`; RED=`tput setaf 1`

install_output_helper() { curl --silent "$OUTPUT_HELPER_URL" -o "$OUTPUT_HELPER_FILE"; }

[[ ! -d "$BASH_LIB_DIR" ]] && mkdir -p "$BASH_LIB_DIR"
[[ ! -f "$OUTPUT_HELPER_FILE" ]] && install_output_helper

source "$OUTPUT_HELPER_FILE"

#---------------
# Vars
#---------------
TASK=${1}
ARGS=${@:2}

PWD=$( pwd )
original_dir="${PWD}"
scratch_dir=""

VERSION="0.2.0"
DOCKER_IMAGE="jimsmyth/scaffold:${VERSION}"

DOCKER_BIN="docker"
DOCKER_BUILD="${DOCKER_BIN} build"
DOCKER_RUN="${DOCKER_BIN} run"
DOCKER_RUN_IT="${DOCKER_RUN} -it"
DOCKER_INSPECT="${DOCKER_BIN} inspect"

DOCKER_SOCK="-v /var/run/docker.sock:/var/run/docker.sock"
DOCKER_GITCONFIG="-v $HOME/.gitconfig:/root/.gitconfig"
DOCKER_SSHDIR="-v $HOME/.ssh:/root/.ssh"
DOCKER_GNUPGDIR="-v $HOME/.gnupg:/root/.gnupg"
DOCKER_GPG_SOCK="$HOME/.gnupg/S.gpg-agent"

#---------------
# Methods
#---------------
usage() {
    echo "USAGE:"
    echo "$0 SUBCOMMAND"
    echo ""
    echo "SUBCOMMANDS:"
    echo "  build-images    Build Docker Images"
    echo "                  EX: $ $0 build-images"
    echo ""
    echo "  scaffold-flask  Scaffold a New Flask App"
    echo "                  EX: $ $0 scaffold-flask"
    echo ""
    echo "  help            Show this output"
    echo ""  
}

cleanup() {
  log rocket "cleanup() fired! Contact foo@example.com if you need assistance."
  if [[ $scratch_dir ]]; then
    log clean "Removing scratch dir: $scratch_dir"
    rm -rf "$scratch_dir"
  fi
  log clean "Going back to original dir: $original_dir"
  cd $original_dir
}

# Docker build and run commands for scaffold
build_images() {
    ARG_VCS_REF="--build-arg VCS_REF=$( git rev-parse --short HEAD )"
    ARG_BUILD_DATE="--build-arg BUILD_DATE=$( date -u +'%Y-%m-%dT%H:%M:%SZ' )"
    ARG_VERSION="--build-arg VERSION=${VERSION}"

    log info "Building Docker Images"
    log check "Building docker image: $DOCKER_IMAGE"
    DOCKER_ARGS="$ARG_VCS_REF $ARG_BUILD_DATE $ARG_VERSION"
    DOCKER_BUILD_CMD="$DOCKER_BUILD -t $DOCKER_IMAGE -f Dockerfile $DOCKER_ARGS ."
    log blank "Docker Command: $DOCKER_BUILD_CMD"
    $DOCKER_BUILD_CMD
}
scaffold_flask() {
    scratch_dir="$( mktemp -d ${original_dir}/tmp-scaffold-create-api.XXXXXXX )"
    trap cleanup EXIT

    DOCKER_SCRATCH_DIR="-v $scratch_dir:$scratch_dir --env scratch_dir=$scratch_dir"

    DOCKER_CMD="$DOCKER_RUN_IT --rm -v ${PWD}:/build -w /build $DOCKER_SCRATCH_DIR"
    $DOCKER_CMD $DOCKER_IMAGE python3 generate_cookiecutter_json.py

    DOCKER_CMD="$DOCKER_RUN_IT --rm -v ${PWD}:/build -w /build -v ${HOME}/.gitconfig:/home/sid/.gitconfig -v ${HOME}/.ssh:/home/sid/.ssh -v ${HOME}/.netrc:/home/sid/.netrc $DOCKER_SCRATCH_DIR"
    $DOCKER_CMD $DOCKER_IMAGE cookiecutter gh:jsmyth/cookiecutter-flask \
                                           --config-file "${scratch_dir}/cookiecutter.yaml" \
                                           --output-dir "${scratch_dir}" \
                                           --no-input
}

case $TASK in
    build_images|build-images)
      build_images ;;
    scaffold_flask|scaffold-flask)
      scaffold_flask ;;
    help)
      usage
      exit 0 ;; 
    *)
      usage
      exit 1 ;;
esac
