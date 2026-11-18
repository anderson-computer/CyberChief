#!/usr/bin/env bash
# ============================================================
# CyberChief: Defender of the Network
# Linux Installer
# Created by Mike Anderson
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default install location
INSTALL_DIR="$HOME/CyberChief"

echo ""
echo " ====================================================="
echo "  CYBERCHIEF: DEFENDER OF THE NETWORK"
echo "  Linux Installer — Created by Mike Anderson"
echo " ====================================================="
echo ""
echo " Default install location: $INSTALL_DIR"
echo ""
read -r -p " Press ENTER to accept, or type a custom path: " CUSTOM_PATH
[ -n "$CUSTOM_PATH" ] && INSTALL_DIR="$CUSTOM_PATH"

echo ""
echo " Installing to: $INSTALL_DIR"

# Create directories
mkdir -p "$INSTALL_DIR/issues"
mkdir -p "$INSTALL_DIR/art"

# Copy files
echo " Copying comic files..."
cp -r "$SRC_DIR/issues/"* "$INSTALL_DIR/issues/"
echo " Copying artwork..."
cp -r "$SRC_DIR/art/"* "$INSTALL_DIR/art/"

# Create launcher script
cat > "$INSTALL_DIR/cyberchief" << 'LAUNCHER'
#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX="$DIR/issues/index.html"
if command -v xdg-open &>/dev/null; then
    xdg-open "$INDEX"
elif command -v firefox &>/dev/null; then
    firefox "$INDEX"
elif command -v google-chrome &>/dev/null; then
    google-chrome "$INDEX"
elif command -v chromium-browser &>/dev/null; then
    chromium-browser "$INDEX"
else
    echo "Open this file in your browser: $INDEX"
fi
LAUNCHER
chmod +x "$INSTALL_DIR/cyberchief"

# Symlink to ~/bin if it exists
if [ -d "$HOME/bin" ]; then
    ln -sf "$INSTALL_DIR/cyberchief" "$HOME/bin/cyberchief"
    echo " Launcher linked: ~/bin/cyberchief"
fi

# Create .desktop file (GNOME/KDE/etc. app menu)
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

# Find icon
ICON="$INSTALL_DIR/art/v2/CyberChief Logo.png"
[ ! -f "$ICON" ] && ICON="application-x-executable"

cat > "$DESKTOP_DIR/cyberchief.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=CyberChief: Defender of the Network
GenericName=Comic Series
Comment=CyberChief cybersecurity comic series by Mike Anderson
Exec=bash "$INSTALL_DIR/cyberchief"
Icon=$ICON
Terminal=false
Categories=Education;Comics;
Keywords=cyberchief;comic;cybersecurity;network;
StartupNotify=true
DESKTOP

chmod +x "$DESKTOP_DIR/cyberchief.desktop"

# Refresh app database if available
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Create uninstaller
cat > "$INSTALL_DIR/uninstall.sh" << UNINSTALL
#!/usr/bin/env bash
echo "Uninstalling CyberChief: Defender of the Network..."
read -r -p "Are you sure? This deletes all files. [y/N]: " CONFIRM
if [[ "\$CONFIRM" =~ ^[Yy]\$ ]]; then
    rm -f "$HOME/.local/share/applications/cyberchief.desktop"
    rm -f "$HOME/bin/cyberchief"
    rm -rf "$INSTALL_DIR"
    echo "Uninstall complete."
else
    echo "Uninstall cancelled."
fi
UNINSTALL
chmod +x "$INSTALL_DIR/uninstall.sh"

echo ""
echo " ====================================================="
echo "  Installation Complete!"
echo " ====================================================="
echo ""
echo "  Location  : $INSTALL_DIR"
echo "  App Menu  : CyberChief: Defender of the Network"
echo "  Command   : cyberchief  (if ~/bin is in your PATH)"
echo "  Uninstall : $INSTALL_DIR/uninstall.sh"
echo ""
echo " Opening CyberChief now..."
echo ""

bash "$INSTALL_DIR/cyberchief"
