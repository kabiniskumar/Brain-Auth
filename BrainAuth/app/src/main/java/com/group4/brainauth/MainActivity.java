package com.group4.brainauth;

import android.Manifest;
import android.content.pm.PackageManager;
import android.content.res.Resources;
import android.os.Environment;
import android.preference.PreferenceActivity;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.json.JSONException;
import org.json.JSONObject;
import cz.msebera.android.httpclient.Header;

public class MainActivity extends AppCompatActivity {
    String[] permissions = new String[]{
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.INTERNET
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        checkPermissions();
        createDir();
    }

    private boolean checkPermissions() {
        int result;
        List<String> listPermissionsNeeded = new ArrayList<>();
        for (String p : permissions) {
            result = ContextCompat.checkSelfPermission(this, p);
            if (result != PackageManager.PERMISSION_GRANTED) {
                listPermissionsNeeded.add(p);
            }
        }
        if (!listPermissionsNeeded.isEmpty()) {
            ActivityCompat.requestPermissions(this, listPermissionsNeeded.toArray(new String[listPermissionsNeeded.size()]), 100);
            return false;
        }
        return true;
    }

    public void createDir(){
        File f = new File(Environment.getExternalStorageDirectory(), "BrainAuth");

        if (!f.exists()) {
            f.mkdirs();
        }
    }
    public void authenticate(View view){
        EditText editText = findViewById(R.id.userName);
        String actualUser = editText.getText().toString().replaceAll(" ","");

        if (actualUser.equals("")){
            Toast t = Toast.makeText(getApplicationContext(),"Enter user name", Toast.LENGTH_LONG);
            t.show();
        }
        else{
            // pick random file
            // send it to server
            // display the contents
            UserMapSingleton instance = new UserMapSingleton();
            instance.getInstance();

            ArrayList<String> fileUser = instance.getRandomFile();
            String file = fileUser.get(0);
            String user = fileUser.get(1);

            uploadToServer(file, user, actualUser);
        }
    }

    public void uploadToServer(String file, final String user, final String actualUser){
        final HashMap<String, String> labelMap = new HashMap<>();
        labelMap.put("1","Jane");
        labelMap.put("2","Rachel");
        labelMap.put("3","Francis");

        try{
            Resources res = getApplicationContext().getResources();
            int id = res.getIdentifier(file.toLowerCase(), "raw", getApplicationContext().getPackageName());
            String dispMessage = "Random EEG file picked: " + user;
            Toast t = Toast.makeText(getApplicationContext(), dispMessage, Toast.LENGTH_LONG);
            t.show();
            InputStream inputStream = getResources().openRawResource(id);

            File f = new File(Environment.getExternalStorageDirectory().getPath() + "/BrainAuth/"
                    +file);
            OutputStream out=new FileOutputStream(f);
            byte buf[]=new byte[3072];
            int len;
            while((len=inputStream.read(buf))>0)
                out.write(buf,0,len);
            out.close();
            inputStream.close();
        }catch (Exception e){
            e.printStackTrace();
        }

        File f = new File(Environment.getExternalStorageDirectory().getPath() + "/BrainAuth/"
                +file);

        RequestParams params = new RequestParams();
        try{
            params.put("file",f);
        }catch (Exception e){
            e.printStackTrace();
        }

        AsyncHttpClient client = new AsyncHttpClient();
        client.post("http://9efeb769.ngrok.io" +"/authenticate", params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] bytes) {
                if(statusCode==200) {
                    try {
                        JSONObject json =new JSONObject(new String(bytes));
                        String prediction = json.getString("1");
                        String logged_in_user_id = labelMap.get(prediction);
                        Toast toast = null;
                        if(logged_in_user_id.equals(actualUser)){
                            toast = Toast.makeText(getApplicationContext(), "AUTHENTICATION SUCCESSFUL", Toast.LENGTH_LONG);
                        }else{
                            toast = Toast.makeText(getApplicationContext(), "AUTHENTICATION FAILED", Toast.LENGTH_LONG);
                        }
                        toast.show();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
                else {
                    Toast.makeText(getApplicationContext(), "Failed", Toast.LENGTH_SHORT).show();
                }
            }
            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] bytes, Throwable throwable) {
                Log.e("Failed",statusCode+"");
                Toast.makeText(getApplicationContext(), "Something Went Wrong", Toast.LENGTH_SHORT).show();

            }
            @Override
            public void onProgress(long bytesWritten, long totalSize) {
                super.onProgress(bytesWritten, totalSize);
            }

            @Override
            public void onStart() {
                super.onStart();
            }

            @Override
            public void onFinish() {
                super.onFinish();
            }
        });
    }
}
