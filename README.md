# Custom Integration Wheels

Home Assistant uses Python wheels with the `musllinux` platform tag for integrations. All libraries required by your custom component must provide wheels, and if they include binaries, they should have the `musllinux` platform tag. If you maintain the library, you can upload `musllinux` wheels as part of the PyPI release.

Sometimes integrations require third-party libraries that don't provide wheels with the `musllinux` platform tag, or any wheels at all. In such cases, you can create a PR which includes the library in the `requirements.txt` file of this repository. Our GitHub Actions will then build the appropriate wheels for that library with the correct platform tag, upload them to our wheels server at https://wheels.home-assistant.io/, and ensure they are used by Home Assistant Core builds in place of the PyPI versions.
