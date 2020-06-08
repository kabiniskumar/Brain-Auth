package com.group4.brainauth;

import android.util.Log;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

public class UserMapSingleton {

    private static UserMapSingleton instance = null;
    public HashMap<String, String> map = new HashMap<>();

    protected UserMapSingleton() {
        // do nothing
    }

    public static UserMapSingleton getInstance() {
        if(instance == null) {
            instance = new UserMapSingleton();
        }
        return instance;
    }

    public void setMap(){
        map.put("S001R03", "Jane");
        map.put("S001R04", "Jane");
        map.put("S002R03", "Rachel");
        map.put("S002R04", "Rachel");
        map.put("S003R03", "Francis");
        map.put("S003R04", "Francis");
    }

    public ArrayList<String> getRandomFile()
    {
        ArrayList<String> output = new ArrayList<>();
        setMap();
        List<String> keysAsArray = new ArrayList<>(map.keySet());
        Random r = new Random();
        String randomFile = keysAsArray.get(r.nextInt(keysAsArray.size()));
        String user = map.get(randomFile);
        output.add(randomFile);
        output.add(user);
        return output;
    }

}
