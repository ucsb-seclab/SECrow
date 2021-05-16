    Activity2.sendRequest.overload('java.net.HttpURLConnection', 'org.json.JSONArray').implementation = function(v1, v2) {
        console.log('\\n\\n\\n\\n---------------------');
        send('sendRequest(http, JSONArray) is called: ' + v1)

        console.log('\\n\\nContents are: ' + v2.toString());

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        console.log('call stack:\\n' + full_call_stack);

    };

    Activity2.sendRequest.overload('java.net.HttpURLConnection', 'org.json.JSONObject', 'java.lang.String').implementation = function(v1, v2, v3) {
        console.log('\\n\\n\\n\\n---------------------');
        send('sendRequest(http, JSONObject, String) is called: ' + v1)

        console.log('\\n\\nContents are: ' + v2.toString());
        console.log('\\n\\nString Content is:' + v3);

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        console.log('call stack:\\n' + full_call_stack);

    };

    Activity2.sendRequest.overload('java.net.HttpURLConnection').implementation = function(v1) {
        console.log('\\n\\n\\n\\n---------------------');
        send('sendRequest(http) is called: ' + v1)

        var stack = threadinstance.currentThread().getStackTrace()
        var full_call_stack = Where(stack)

        console.log('call stack:\\n' + full_call_stack);

    };