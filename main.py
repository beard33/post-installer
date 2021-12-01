import json
import helper
import tui
import os

helper = helper.Helper()

# Check sudo permissions
tui.print_info("♦ Checking sudo permissions...")
if(not helper.is_sudo()):
    tui.print_error("Please run the script with sudo permissions!")
    exit(1)
tui.print_ok("ok")

# TODO add manual input for distro
# Detect the distribution
tui.print_bold("♦ Detected -> " + helper.Distro.upper() + 
             "\n♦ Package manager -> " + helper.PackageManager.upper())
if(not tui.user_continue()):
    tui.print_warning("Bye!")
    exit(0)

# Read the appropriate json
commands = {}
sw_list = "lists/" + helper.Distro + ".json"
with open(sw_list, 'r') as f:
    data = json.load(f)

# TODO add flatpak / snap support
for category in data:
    tui.print_bold(f"\nThe following {category} softwares are going to be installed:")
    for package in data[category]:
        if data[category][package]:
            tui.print_warning(f"♦ {package}")
            commands[package] = helper.build_std_command(package)
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
