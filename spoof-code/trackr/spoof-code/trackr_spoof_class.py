import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


singlecode = """
Java.perform(function () {
    // Function to hook is defined here
    var MainActivity = Java.use('com.phonehalo.trackr.TrackrItem');
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

    MainActivity.setBluetoothAddress.overload('java.lang.String').implementation = function(v1) {
        console.log('\\n\\n\\n\\n---------------------');
        send('setBluetoothAddress is called: ');

        console.log('v1 :' + v1.toString());
        //v1 = "DA:1B:6E:2D:43:E4";
        v1 = "F3:1B:61:69:51:71"
        console.log('changed v1 :' + v1.toString());
        console.log('\\n\\n\\n\\n---------------------');
        return MainActivity.setBluetoothAddress.overload('java.lang.String').call(this, v1);
    }

    MainActivity.setTrackrId.overload('java.lang.String').implementation = function(v1) {
        console.log('\\n\\n\\n\\n---------------------');
        send('setTrackrID is called: ');

        console.log('v1 :' + v1.toString());
        v1 = "00007151-69611bf3";
        console.log('changed v1 :' + v1.toString());
        console.log('\\n\\n\\n\\n---------------------');
        return MainActivity.setTrackrId.overload('java.lang.String').call(this, v1);
    }

    });
"""



jscode = """
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
            //'com.phonehalo.ble.service.PHBleServiceClient',
        ].forEach(traceClass);

    //traceMethodInClass('com.phonehalo.ble.service.PHBleServiceClient', 'requestRssiUpdate');
    //traceMethodInClass('com.phonehalo.trackr.TrackrItem', '$init');
    traceMethodInClass('com.phonehalo.ble.service.PHBleServiceClient$OfficialServiceReceiver', 'onReceive');

    });
};

Java.perform(Main);

"""

process = frida.get_usb_device().attach('com.phonehalo.itemtracker')
script = process.create_script(singlecode)
script.on('message', on_message)
print('[*] Running Trckr')
script.load()
sys.stdin.read()
