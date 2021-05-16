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
    /*
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
    */


    var activity2 = Java.use('j.a.a.a');

    // the first argument contains string that has mac address
    activity2.h.overload().implementation = function() {
        console.log('---------------------\\n\\n\\n\\n');
        console.log('Calling j.a.a.a.h -- getBluetoothMacAddress');

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        var retval = "D8:01:00:00:1D:7E";
        //return this.activity2.h.overload().call(this);
        console.log('Retval: ' + retval);

        console.log("call stack:\\n\\n" + full_call_stack);
        console.log('---------------------\\n\\n\\n\\n');
        return retval;
    };
});
"""



classcode = """
var Color = {
    RESET: "\x1b[39;49;00m", Black: "0;01", Blue: "4;01", Cyan: "6;01", Gray: "7;11", Green: "2;01", Purple: "5;01", Red: "1;01", Yellow: "3;01",
    Light: {
        Black: "0;11", Blue: "4;11", Cyan: "6;11", Gray: "7;01", Green: "2;11", Purple: "5;11", Red: "1;11", Yellow: "3;11"
    }
};

/**
 *
 * @param input. 
 *      If an object is passed it will print as json 
 * @param kwargs  options map {
 *     -l level: string;   log/warn/error
 *     -i indent: boolean;     print JSON prettify
 *     -c color: @see ColorMap
 * }
 */
var LOG = function (input, kwargs) {
    kwargs = kwargs || {};
    var logLevel = kwargs['l'] || 'log', colorPrefix = '\x1b[3', colorSuffix = 'm';
    if (typeof input === 'object')
        input = JSON.stringify(input, null, kwargs['i'] ? 2 : null);
    if (kwargs['c'])
        input = colorPrefix + kwargs['c'] + colorSuffix + input + Color.RESET;
    console[logLevel](input);
};

var printBacktrace = function () {
    Java.perform(function() {
        var android_util_Log = Java.use('android.util.Log'), java_lang_Exception = Java.use('java.lang.Exception');
        // getting stacktrace by throwing an exception
        LOG(android_util_Log.getStackTraceString(java_lang_Exception.$new()), { c: Color.Gray });
    });
};

function traceClass(targetClass) {
    var hook;
    try {
        hook = Java.use(targetClass);
    } catch (e) {
        console.error("trace class failed", e);
        return;
    }

    var methods = hook.class.getDeclaredMethods();
    hook.$dispose();

    var parsedMethods = [];
    methods.forEach(function (method) {
        var methodStr = method.toString();
        var methodReplace = methodStr.replace(targetClass + ".", "TOKEN").match(/\sTOKEN(.*)\(/)[1];
         parsedMethods.push(methodReplace);
    });

    uniqBy(parsedMethods, JSON.stringify).forEach(function (targetMethod) {
        traceMethod(targetClass + '.' + targetMethod);
    });
}

function traceMethodInClass(targetClass, targetMethod) {
    var hook;
    try {
        hook = Java.use(targetClass);
    } catch (e) {
        console.error("trace class failed", e);
        return;
    }

    traceMethod(targetClass + '.' + targetMethod);
}

function traceMethod(targetClassMethod) {
    var delim = targetClassMethod.lastIndexOf('.');
    if (delim === -1)
        return;

    var targetClass = targetClassMethod.slice(0, delim);
    var targetMethod = targetClassMethod.slice(delim + 1, targetClassMethod.length);

    var hook = Java.use(targetClass);
    var overloadCount = hook[targetMethod].overloads.length;

    LOG({ tracing: targetClassMethod, overloaded: overloadCount }, { c: Color.Green });

    for (var i = 0; i < overloadCount; i++) {
        hook[targetMethod].overloads[i].implementation = function () {
            var log = { '#': targetClassMethod, args: [] };

            for (var j = 0; j < arguments.length; j++) {
                var arg = arguments[j];
                // quick&dirty fix for java.io.StringWriter char[].toString() impl because frida prints [object Object]
                if (j === 0 && arguments[j]) {
                    if (arguments[j].toString() === '[object Object]') {
                        var s = [];
                        for (var k = 0, l = arguments[j].length; k < l; k++) {
                            s.push(arguments[j][k]);
                        }
                        arg = s.join('');
                    }
                }
                log.args.push({ i: j, o: arg, s: arg ? arg.toString(): 'null'});
            }

            var retval;
            try {
                retval = this[targetMethod].apply(this, arguments); // might crash (Frida bug?)
                log.returns = { val: retval, str: retval ? retval.toString() : null };
            } catch (e) {
                console.error(e);
            }
            send('---------------------------')
            LOG(log, { c: Color.Blue });
            printBacktrace();
            send('---------------------------\\n\\n')
            return retval;
        }
    }
}

// remove duplicates from array
function uniqBy(array, key) {
    var seen = {};
    return array.filter(function (item) {
        var k = key(item);
        return seen.hasOwnProperty(k) ? false : (seen[k] = true);
    });
}


var Main = function() {
    Java.perform(function () { // avoid java.lang.ClassNotFoundException
        [
            //'java.io.BufferedWriter',
            //'java.io.BufferedReader',
            //'j.a.c.f.d',
            //'net.chipolo.model.net.data.NetChipolo',
            //'net.chipolo.model.net.data.NetChipoloData',
            //'j.a.d.b.b',
            //'java.net.HttpURLConnection',
            //'l.c0$a',
            //'l.a0',
            //'j.a.a.a',
            //'l.c0',
        ].forEach(traceClass);

    // to hook into specific functions in a specific class
    //traceMethodInClass('j.a.c.f.b$c', 'toString');
    //traceMethodInClass('net.chipolo.app.e.d.a', 'a');
    //traceMethodInClass('j.a.a.f.f$j', 'toString');
    
    //traceMethodInClass('l.c0$a', 'a');
    //traceMethodInClass('l.c0', 'toString');
    
    //traceMethodInClass('l.h0.g.b', 'a');
    //traceMethodInClass('l.h0.g.g', 'a');
    //traceMethodInClass('l.h0.f.a', 'a');
    //traceMethodInClass('l.h0.e.a', 'a');
    //traceMethodInClass('l.h0.g.j', 'a');
    //traceMethodInClass('d.g.a.a', 'a');
    //traceMethodInClass('j.a.c.f.d', 'a');
    //traceMethodInClass('j.a.c.f.a', 'a');
    //traceMethodInClass('l.z', 'a');
    //traceMethodInClass('l.z$b', 'b');
    //traceMethodInClass('l.h0.b', 'run');
    
    //traceMethodInClass('l.h0.g.g', 'a'); // this is imp
    //traceMethodInClass('j.a.a.a', 'b');   // blutooth mac adress return
    //traceMethodInClass('j.a.a.a', '$init');   // blutooth mac adress return
    //traceMethodInClass('net.chipolo.model.model.u', 'a');
    
    traceMethodInClass('net.chipolo.ble.chipolo.l', 'onLeScan');
    //traceMethodInClass('j.a.c.f.d$b', 'a');
    
    
    //traceMethodInClass('net.chipolo.ble.chipolo.f', '$init');


        /*
        Java.use('java.net.Socket').isConnected.overload().implementation = function () {
            LOG('Socket.isConnected.overload', { c: Color.Light.Cyan });
            printBacktrace();
            return true;
        }
        */

        
    //var activity = Java.use('net.chipolo.ble.chipolo.l');

    /*    
    Java.use('net.chipolo.ble.chipolo.l').c.overload('java.lang.String', 'java.lang.String', '[B').implementation = function(v1, v2, v3) {
        console.log('\\n\\n\\n\\n---------------------');
        LOG('net.chipolo.ble.chipolo.l.c.overload', { c: Color.Light.Cyan });
        if (v1 == "D8:01:00:00:1F:79") {
            LOG('Changing MAC and Bytes', { c: Color.Light.Yellow });
            console.log("\\nOriginal MAC: " + v1);

            
            // Device 1
            v1 = "D8:01:00:00:1E:33";
            //v3 = Java.array('byte', [2,1,6,5,3,101,-2,51,-2,13,22,51,-2,1,1,1,0,-40,1,0,0,30,51,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]);
            v3 = Java.array('byte', [2,1,6,5,3,101,-2,51,-2,13,22,51,-2,1,3,1,0,-40,1,0,0,31,121,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]);

            

            // Device 2
            v1 = "D8:01:00:00:1D:7E";
            //v3 = Java.array('byte', );


            console.log("\\nChanged MAC: " + v1);
        }
        
        console.log("v1: " + v1 + "\\nv2: " + v2 + "\\nv3: " + v3);

        console.log('---------------------\\n\\n\\n\\n');

        //return this.c.overload('java.lang.String', 'java.lang.String', '[B').call(this, v1, v2, v3);
        return this.c(v1, v2, v3);
    }
    */
    
    Java.use('net.chipolo.ble.chipolo.l').onLeScan.overload('android.bluetooth.BluetoothDevice', 'int', '[B').implementation = function(v1, v2, v3) {
        console.log('\\n\\n\\n\\n---------------------');
        console.log('onLeScan called: \\n\\n');
        console.log('v1 is: ' + v1.getAddress());
        v1= "D8:01:00:00:1E:33";

        return this.call(this, v1, v2, v3);
    }

    });
};

Java.perform(Main);

"""



process = frida.get_usb_device().attach('chipolo.net.v3')
script = process.create_script(classcode)
script.on('message', on_message)
print('[*] Running Chipolo')
script.load()
sys.stdin.read()
