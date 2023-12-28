# SpearHandler
 Spear & Shield Python Backend

# Installation and Setup
This requires quite a few librares, notably
- requests
- pymetasploit3 (must be installed through the source and NOT pip!) (as of 12/28/2023)
- mythic (which requires microsoft visual c++ build tools) (to install, you have to go into the installer, click modify, then install) (if you run into issue with the c++ command, try installing aiohttp)

A problem with the fact that SpearHandler integrates so many tools together, is that version handling becomes quite a nightmare due to edge cases and bugs in other libraries. Errors are to be expected when installing.