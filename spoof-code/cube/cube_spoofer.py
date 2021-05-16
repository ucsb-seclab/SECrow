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

    */

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
    
    var Activity3 = Java.use('com.blueskyhomesales.cube.service.BleProfileService');

    Activity3.a.overload('int', 'int', 'java.lang.String').implementation = function(v1, v2, v3) {
       console.log('\\n\\n\\n\\n---------------------');
        send('a from BleProfileService is called: ');

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        console.log('v1: ' + v1.toString());
        console.log('v2: ' + v2.toString());
        console.log('v3: ' + v3.toString());

        console.log("call stack:\\n" + full_call_stack);

        return Activity3.a.overload('int', 'int', 'java.lang.String').call(this, v1, v2, v3);
    };

    var BoundDeviceAct = Java.use('com.blueskyhomesales.cube.utility.bean.BoundDevice');

    BoundDeviceAct.toString.overload().implementation = function() {
        console.log('\\n\\n\\n\\n------------------');
        send('toString is called: ');

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        console.log("call stack:\\n" + full_call_stack);

        var retval = BoundDeviceAct.toString.overload().call(this);
        console.log("return value: " + retval);

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
            //'com.phonehalo.ble.base.BleManager$Request',
            //'com.blueskyhomesales.cube.activity.NetCreateAccountActivity',
            //'com.blueskyhomesales.cube.application.MyApplication',
            //'com.blueskyhomesales.cube.b.a',
            //'com.blueskyhomesales.cube.domain.BleDeviceManager',
            //'com.blueskyhomesales.cube.database.a',
            //'com.blueskyhomesales.cube.database.b',
            //'com.blueskyhomesales.cube.database.c',
            //'com.blueskyhomesales.cube.database.d',
            //'com.blueskyhomesales.cube.database.e',
            //'com.blueskyhomesales.cube.database.f',
            //'com.blueskyhomesales.cube.database.g',
            //'com.blueskyhomesales.cube.service.a$b',
            //'java.io.BufferedWriter',
            //'java.io.BufferedReader',
            //'com.blueskyhomesales.cube.g.i',
            //'com.blueskyhomesales.cube.database.LostRecordData',
            //'okhttp3.e0.e.a',
            //'okhttp3.HttpUrl',
            //'okhttp3.HttpUrl$Builder',
            //'okhttp3.internal.http2.d',
            //'com.blueskyhomesales.cube.e.a',
            //'okhttp3.internal.connection.c',
        ].forEach(traceClass);

    // to hook into specific functions in a specific class
    // traceMethodInClass('com.phonehalo.ble.official.OfficialService', 'onCreate');
    //traceMethodInClass('com.blueskyhomesales.cube.database.LostRecordData', 'toString');
    //traceMethodInClass('com.blueskyhomesales.cube.database.LostRecordData', 'writeToParcel');
    traceMethodInClass('com.blueskyhomesales.cube.e.a', 'a');
    //traceMethodInClass('okhttp3.HttpUrl$Builder', '$init');
    //traceMethodInClass('okhttp3.e0.f.g', 'a');
    //traceMethodInClass('com.blueskyhomesales.cube.utility.bean.BoundDevice', 'toString');
    //traceMethodInClass('com.blueskyhomesales.cube.service.BleProfileService', 'a');
    //traceMethodInClass('e.m', '$init');
    traceMethodInClass('com.blueskyhomesales.cube.utility.bean.PersonalInfoBean', 'setOldDeviceNumber');
    traceMethodInClass('com.blueskyhomesales.cube.utility.bean.PersonalInfoBean', 'getOldDeviceNumber');

        /*
        Java.use('java.net.Socket').isConnected.overload().implementation = function () {
            LOG('Socket.isConnected.overload', { c: Color.Light.Cyan });
            printBacktrace();
            return true;
        }
        */
    });
};

Java.perform(Main);

"""



process = frida.get_usb_device().attach('com.blueskyhomesales.cube')
script = process.create_script(classcode)
script.on('message', on_message)
print('[*] Running Cube')
script.load()
sys.stdin.read()
