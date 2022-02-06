import subprocess
import os

class Helper:

    PackageManager = ""
    Distro = ""

    def __init__(self):
        self.detect_distro()
        self.set_package_manager()

    def detect_distro(self) -> str:
        info = subprocess.Popen(
            ['cat', '/etc/os-release'],
            stdout=subprocess.PIPE)
        info = info.communicate()[0].decode('utf-8').split()
        for line in info:
            if line.startswith("ID="):
                self.Distro = line[3:]
                break
            
    def set_package_manager(self):
        if self.Distro in ['fedora', 'redhat'] : self.PackageManager = 'dnf' 
        if self.Distro in ['ubuntu', 'debian', 'pop', 'elementary'] : self.PackageManager = 'apt' 
        if self.Distro in ['arch', 'manjaro', 'endeavouros'] : self.PackageManager = 'pacman'

    def first_update(self) -> str:
        if self.PackageManager == 'pacman':
            return 'sudo pacman -Syu --noconfirm'
        elif self.PackageManager == 'dnf':
            return 'sudo dnf update -y'
        else:
            return 'sudo apt update && sudo apt -y upgrade'

    def build_std_command(self, package :str) -> str:
        if self.PackageManager == 'pacman':
            return 'sudo ' + self.PackageManager + ' -S ' + package + ' --noconfirm'
        else:
            return 'sudo ' + self.PackageManager + ' install ' + package + ' -y'

    def build_flatpak_command(self, package: str) -> str:
        return 'flatpak install ' + package + ' -y'

    def is_sudo(self) -> bool:
        return (os.getuid() == 0)
