## Setup

All the challenges and investigation within Tile required use of a proxy (`mitmproxy`) and making sure you bypass the SSL pinning on the Android device. This way it becomes possible to read all the HTTPS requests being sent through the Tile app to their webserver. 

Tile flow files contain the mitmproxy files that can be read using `mitmweb` binary.
