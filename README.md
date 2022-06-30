# Custom Integration Wheels

Home Assistant uses musllinux wheels for the integration. For your custom component library, you need to provide any wheels, or if they include binaries, musllinux wheels. You can upload this as well with the release to PyPI.

Sometimes you need 3-party library they don't want provide musllinux or any wheels. In that case you can request to add this library into `requirements.txt`
