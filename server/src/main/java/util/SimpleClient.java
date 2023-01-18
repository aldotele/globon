package util;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import java.io.IOException;
import java.util.Map;

public class SimpleClient {
    private static final OkHttpClient client = new OkHttpClient();

    public static Request buildRequest(String url) {
        return new Request.Builder()
        .url(url)
        .build();
    }

    public static Request buildRequest(String url, Map<String, String> headersMap) {
        Request.Builder requestBuilder = new Request.Builder();
        requestBuilder.url(url);
        for (Map.Entry<String, String> entry : headersMap.entrySet()) {
            requestBuilder.addHeader(entry.getKey(), entry.getValue());
        }
        return requestBuilder.build();
    }

    public static Response makeRequest(Request request) throws IOException {
        return client.newCall(request).execute();
    }
    
}
