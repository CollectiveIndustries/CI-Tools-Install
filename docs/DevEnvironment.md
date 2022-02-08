# Development with VS Code

## Setup and Install
A full Linux IDE configuration is included with this repository for development. Running ``InstallVSCode.sh`` will download and import the Microsoft GPG Key for use with the ``apt`` package manager (I run a debian based development system and dont have access to anything RPM Based at the moment), once the keys are downloaded and installed it will update the package cache and install VS Code with all of its dependancies.

## Import Extensions
A list of extensions can be found in the ``vsc-extensions.txt`` file in the root of this repository. This file can be used to import them into VSCode using ``VSC Export & Import``.

+ First navigate to the Extensions tab on the side bar (Ctrl+Shift+X) search for and install ``VSC Export & Import``
+ Once installed open this repository as a folder from the File menu (Ctrl+K Ctrl+O)
+ Use the command pallet (Ctrl+Shift+P) to search for ``VSC Extensions Import``
+ This will automatically load and import the ``vsc-extensions.txt`` from the root of the repository and install the additional extensions.