#!/usr/bin/env bash

INSTALL_DIR="$HOME/.config/bin"
CURRENT_DIR="$(pwd)"

echo "Creating file"

echo "#!/usr/bin/env bash" > "kernel"
echo "$CURRENT_DIR"/jeprnel.py >> "kernel"

chmod +x kernel

mv kernel "$INSTALL_DIR"

echo "Installation finished"
echo "Run kernel to test"
