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
            at = at + stack[i].toString() + ':';
        }
        return at;
    }

    // Whenever button is clicked
    MainActivity.write.overload('java.lang.String', 'int', 'int').implementation = function (v1, v2, v3) {
        // Show a message to know that the function got called
		console.log('\\n\\n\\n\\n---------------------');
        send('write is called:' + v1);
        
        // v1 = 'dsds';
        // v3 = 4;

        var retval = 0;
        
        var stack = threadinstance.currentThread().getStackTrace();
        var full_call_stack = Where(stack);
        
        
        retval = this.write(v1, v2, v3);
        // Log to the console that it's done, and we should have the flag!
        console.log('General Trackr Info:' + v1.toString() + ', arg 2:' + v2 + ', arg 3:' + v3 + ", cll stk:" + full_call_stack);
        
        console.log('Retval:' + retval);
		console.log('\\n\\n\\n\\n---------------------');
		return retval;
    };
    
    /*
    var MainActivity2 = Java.use('java.io.Writer');

    // Whenever button is clicked
    MainActivity2.write.overload('java.lang.String', 'int', 'int').implementation = function (v1, v2, v3) {
        // Show a message to know that the function got called
        send('writer (string, int, int) is called:' + v1);
        
        // v1 = 'dsds';
        // v3 = 4;

        var retval = 0;
        
        var stack = threadinstance.currentThread().getStackTrace();
        var full_call_stack = Where(stack);
        
        retval = this.write(v1, v2, v3);
        // Log to the console that it's done, and we should have the flag!
        console.log('General Trackr Info (wirter string, int, int):' + v1.toString() + ', arg 2:' + v2 + ', arg 3:' + v3 + ", cll stk:" + full_call_stack);
        
        console.log('Retval (writer string, int, int):' + retval);
    };
    
    
    // Whenever button is clicked
    MainActivity2.write.overload('java.lang.String').implementation = function (v1) {
        // Show a message to know that the function got called
        send('writer (string) is called:' + v1);
        
        // v1 = 'dsds';
        // v3 = 4;

        var retval = 0;
        var stack = threadinstance.currentThread().getStackTrace();
        var full_call_stack = Where(stack);
        
        
        retval = this.write(v1);
        // Log to the console that it's done, and we should have the flag!
        console.log('General Trackr Info (wirter string):' + v1.toString() + ', cll stk:' + full_call_stack);
        
        console.log('Retval (writer string):' + retval);
    };
    
    */

	/*
		url.$init.overload('java.lang.String').implementation = function (var0) {
    		var stack = threadinstance.currentThread().getStackTrace();
            var full_call_stack = Where(stack);
			console.log("[*] Created new URL with value: " + var0 + " at " + "\\n\\t Full call stack:" + full_call_stack);
			return this.$init(var0);
		};

		url.openConnection.overload().implementation = function () {
			console.log("[*] Created new URL connection\\n");
			return this.openConnection();
		};

		url.openConnection.overload('java.net.Proxy').implementation = function (var0) {
			console.log("[*] Created new URL connection with proxy value: " + var0 +"\\n");
			return this.openConnection(var0);
		};


		var URLConnection = Java.use("java.net.URLConnection");

		URLConnection.connect.implementation = function () {
			console.log("[*] Connect called.\\n");
			this.connect();
		};

		URLConnection.getContent.overload().implementation = function () {
			var content = this.getContent();
			console.log("[*] Get content called. Content: " + content + "\\n");
			return content;
		};

		URLConnection.getContentType.implementation = function () {
			var contentType = this.getContentType();
			console.log("[*] Get content type called. Content type: " + contentType + "\\n");
			return contentType;
		};

		URLConnection.getContentLength.implementation = function () {
			var contentLength = this.getContentLength();
			console.log("[*] Get content length called. Content length: " + contentLength + "\\n");
			return contentLength;
		};

		URLConnection.getContentLengthLong.implementation = function () {
			var contentLengthLong = this.getContentLengthLong();
			console.log("[*] Get content length long called. Content length long: " + contentLengthLong + "\\n");
			return contentLengthLong;
		};

		URLConnection.getContentEncoding.implementation = function () {
			var contentEncoding = this.getContentEncoding();
			console.log("[*] Get content encoding called. Content encoding: " + contentEncoding + "\\n");
			return contentEncoding;
		};

		URLConnection.getDate.implementation = function () {
			var contentDate = this.getDate();
			console.log("[*] Get date called. Date: " + contentDate + "\\n");
			return contentDate;
		};

		URLConnection.getExpiration.implementation = function () {
			var contentExpiration = this.getExpiration();
			console.log("[*] Get expiration called. Expiration: " + contentExpiration + "\\n");
			return contentExpiration;
		};

		URLConnection.getLastModified.implementation = function () {
			var lastModified = this.getLastModified();
			console.log("[*] Get last modified called. Value: " + lastModified + "\\n");
			return lastModified;
		};

		URLConnection.getInputStream.implementation = function () {
			console.log("[*] Get input stream called.\\n");
			return this.getInputStream;
		};

		URLConnection.setDoOutput.overload('boolean').implementation = function (var0) {
			console.log("[*] URLConnection.setDoOutput called with value: " + var0 + ".\\n");
			this.setDoOutput(var0);
		};

		URLConnection.setDoInput.overload('boolean').implementation = function (var0) {
			console.log("[*] URLConnection.setDoInput called with value: " + var0 + ".\\n");
			this.setDoInput(var0);
		};

		var httpURLConnection = Java.use("com.android.okhttp.internal.huc.HttpURLConnectionImpl");

		httpURLConnection.setRequestMethod.overload('java.lang.String').implementation = function (var0) {
			console.log("[*] Set request method called: " + var0 + "\\n");
			this.setRequestMethod(var0);
		};

		httpURLConnection.setRequestMethod.overload('java.lang.String').implementation = function (var0) {
			console.log("[*] Set request method called: " + var0 + "\\n");
			this.setRequestMethod(var0);
		};	

		httpURLConnection.connect.implementation = function () {
			console.log("[*] Connect called.\\n");
			this.connect();
		};

		httpURLConnection.disconnect.implementation = function () {
			console.log("[*] Disconnect called.\\n");
			this.disconnect();
		};

		httpURLConnection.getResponseCode.implementation = function () {
			var responseCode  = this.getResponseCode();
			console.log("[*] Get response code called: " + responseCode + "\\n");
			return responseCode;
		};

		var httpsURLConnection = Java.use("com.android.okhttp.internal.huc.HttpsURLConnectionImpl");

		httpsURLConnection.setRequestMethod.overload('java.lang.String').implementation = function (var0) {
			console.log("[*] Set request method called: " + var0 + "\\n");
			this.setRequestMethod(var0);
		};

		httpsURLConnection.connect.implementation = function () {
			console.log("[*] Connect called.\\n");
			this.connect();
		};

		httpsURLConnection.disconnect.implementation = function () {
			console.log("[*] Disconnect called.\\n");
			this.disconnect();
		};

		httpsURLConnection.getResponseCode.implementation = function () {
			var responseCode  = this.getResponseCode();
			console.log("[*] Get response code called: " + responseCode + "\\n");
			return responseCode;
		};

		httpsURLConnection.setRequestProperty.overload('java.lang.String', 'java.lang.String').implementation = function (var0, var1) {
			console.log("[*] URLConnection.setRequestProperty called with key: " + var0 + " and value: " + var1 + ".\\n");
			this.setRequestProperty(var0, var1);
		};
		*/
});
"""

process = frida.get_usb_device().attach('com.thetileapp.tile')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running Tile')
script.load()
sys.stdin.read()
