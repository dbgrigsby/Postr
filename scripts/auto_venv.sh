# User specific aliases and functions
has_virtualenv() {
    if [ -e venv ]; then
        deactivate >/dev/null 2>&1
        source bin/activate
    fi
}

venv_cd () {
    cd "$@" && has_virtualenv
}

alias cd="venv_cd"

# https://gist.github.com/alanthonyc/1048701