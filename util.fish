#!/bin/fish

# script hecho en fish-shell para crear atajos para el proyecto
# 
# - dependencias (paquetes linux):
#     - python
#     - fish
#
# - dependencias (pip):
#     - python-facebook-api
#     - python-dotenv
#
# - uso:
#     - ./util.fish --init
#           -> instala el entorno virtual en ./venv
#     - ./util.fish --setup
#           -> actualiza pip virtual e instala las dependencias
#     - ./util.fish --run
#           -> ejecuta el programa

# obtener el path relativo al script
set REL_ROOT_DIR (dirname (status --current-filename))

# obtener el path absoluto al script
set ABS_ROOT_DIR ( 
    set relativePath $REL_ROOT_DIR
    set currentPath (pwd)
    cd $relativePath
    set absolutePath (pwd)
    cd $currentPath
    echo $absolutePath
)

# alias correctos
function pip
    "$ABS_ROOT_DIR/venv/bin/pip" $argv
end

function python
    "$ABS_ROOT_DIR/venv/bin/python" $argv
end


switch $argv[1]

    case "--init"
        python -m venv $ABS_ROOT_DIR/venv

    case "--setup"
        python -m pip install --upgrade pip

        pip install --upgrade \
            python-facebook-api \
            python-dotenv
    
    case "--run"
        set python "$ABS_ROOT_DIR/venv/bin/python"
        
        python main.py
end