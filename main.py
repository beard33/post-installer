import json
import helper
import tui
import os

helper = helper.Helper()
flatpak = False

# Check sudo permissions
tui.print_info("♦ Checking sudo permissions...")
if(not helper.is_sudo()):
    tui.print_error("Please run the script with sudo permissions!")
    exit(1)
tui.print_ok("ok")

# TODO add manual input for distro
# Detect the distribution
distro = helper.Distro.upper()
pm = helper.PackageManager.upper()

tui.print_bold("♦ Detected -> " + distro + 
             "\n♦ Package manager -> " + pm)
if(not tui.user_continue()):
    tui.print_warning("Bye!")
    exit(0)
if (distro == 'FEDORA'):
    tui.print_bold("♦ Your distro supports Flatpak. Procede with the relative JSON?")
    flatpak = tui.user_continue()

# Read the appropriate json
commands = {}
flatpak_commands = {}

sw_list = "lists/" + helper.Distro + ".json"
with open(sw_list, 'r') as f:
    data = json.load(f)

# Read if supported the flatpak list
if (flatpak):
    flatpak_sw_list = "lists/flatpak.json"
    with open(flatpak_sw_list, 'r') as f:
       flatpak_data = json.load(f)

# TODO add flatpak / snap support
tui.print_header('Standard ' + pm)
for category in data:
    tui.print_bold(f"\nThe following {category} are going to be installed:")
    for package in data[category]:
        if data[category][package]:
            tui.print_warning(f"♦ {package}")
            commands[package] = helper.build_std_command(package)
if (flatpak):
    tui.print_header('Flatpak')
    for category in flatpak_data:
        tui.print_bold(f"\nThe following {category} are going to be installed:")
        for package in flatpak_data[category]:
            if flatpak_data[category][package]:
                tui.print_warning(f"♦ {package}")
                flatpak_commands[package] = helper.build_flatpak_command(package)
                
if(not tui.user_continue()):
    tui.print_warning("Bye!")
    exit(0)

# Update the fresh installed distro
tui.print_bold("Performing a first update...")
exit_code = os.system(helper.first_update())
if (exit_code != 0):
    tui.print_error("Somehing went wrong!")
    exit(1)
tui.print_ok("Done")

# Install selected packages
for package in commands:
    tui.print_warning(f"Installing {package}...")
    exit_code = os.system(commands[package])
    if (exit_code != 0):
        tui.print_error("Somehing went wrong!")
        exit(1)

tui.print_ok('All packages have been succesfully installed!\n')
