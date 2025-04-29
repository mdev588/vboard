# vboard
*A virtual keyboard for Linux with Wayland support and extensive customization options.*


<img src="https://github.com/user-attachments/assets/66e9a879-c677-429f-bd11-503d10e63c2b" width="400">

## Overview
vboard is a lightweight, customizable virtual keyboard designed for Linux systems with Wayland support. It provides an on-screen keyboard solution that's especially useful for:

- Touchscreen devices without physical keyboards
- Systems with malfunctioning physical keyboards
- Accessibility needs
- Kiosk applications

The keyboard supports customizable colors, opacity settings, and can be easily modified to support different layouts.

## Features
- **Customizable appearance**: Change background color, text color, and opacity
- **Persistent settings**: Configuration is saved between sessions
- **Modifier key support**: Use Shift, Ctrl, Alt and Super keys
- **Compact interface**: Headerbar with minimal controls to save screen space
- **Always-on-top**: Stays above other windows for easy access

### **1. Install Dependencies**  
Install  `python-uinput steam-devices` packages using your package manager:  

**For Debian/Ubuntu-based distributions:**  
```bash
sudo apt install python3-uinput steam-devices
```

**For Fedora-based distributions:**  
```bash
sudo dnf install python3-uinput steam-devices
```

**For arch-based distributions:**  
```bash
yay -Syu python-uinput steam-devices
```


### **2. Download vboard**  
Retrieve the latest version of `vboard.py` using `wget`:  
```bash
wget https://github.com/mdev588/vboard/releases/download/v1.17/vboard.py
```



### **3. Run**  

```bash
python3 vboard.py
```

### **4. Create shortcut (optional)**  

```bash
cat > ~/.local/share/applications/vboard.desktop <<EOF
[Desktop Entry]
Exec=bash -c 'python3 ~/vboard.py'
Icon=preferences-desktop-keyboard
Name=Vboard
Terminal=false
Type=Application
Categories=Utility
NoDisplay=false
EOF
```
Make shortcut executable
```
chmod +x ~/.local/share/applications/vboard.desktop
```
Now you should find it in menu insdie Utility section

### Usage
When launched, vboard presents a compact keyboard with a minimal interface. The keyboard includes:
- Standard QWERTY layout keys
- Arrow keys
- Modifier keys (Shift, Ctrl, Alt, Super)

#### Interface Controls
- ☰ (menu) - Toggle visibility of other interface controls
- + - Increase opacity
- - - Decrease opacity
- **Background dropdown** - Change the keyboard background color

### Configuration
vboard saves its settings to ~/.config/vboard/settings.conf. This configuration file stores:
- Background color
- Opacity level
- Text color
- Last window position and size (separately for landscape and portrait orientations)

You can manually edit this file or use the built-in interface controls to customize the appearance.

### Customizing Keyboard Layout
The keyboard layout is defined in the rows list in the source code. To modify the layout:
1. Download the source code
2. Locate the rows definition (around line 175)
3. Modify the key arrangement as needed
4. The format follows a nested list structure where each inner list represents a row of keys

## Troubleshooting
### 1. Error: 'no such device'
 Make sure uinput kernel module is loded with
```bash
sudo modprobe uinput
```

to make sure it auto load on boot create file with
```bash
echo 'uinput' | sudo tee /etc/modules-load.d/module-uinput.conf
```
---
### 2. Error: 'Permission Denied'
Reload udev rules with
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```
---
### 3. Error: 'steam-devices package not found'.
- in Fedora make sure the RPM Fusion repository is enabled. You can follow the guide here:
https://rpmfusion.org/Configuration
- Others can follow steps in here https://github.com/mdev588/vboard/issues/8
## Contributing 
Contributions to vboard are welcome! Here are some ways you can help:

- Add support for more keyboard layouts
- Improve the UI
- Fix bugs or implement new features
- Improve documentation

Please make sure to test your changes before submitting a pull request.

## License
vboard is licensed under the GNU Lesser General Public License v2.1. See LICENSE.md for the full license text.

## Note

* Currently only the QWERTY US layout is supported, so other layouts may cause some keys to produce different keystrokes. But this could easily be fixed by modifying the row list arrangement.

* Currently do not work correctly on wlroots based window managers.

