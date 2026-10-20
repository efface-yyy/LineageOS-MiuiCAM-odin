package com.odin.compat;

import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.OutputConfiguration;
import android.os.Parcel;
import android.util.Log;
import android.view.Surface;
import org.json.*;
import java.io.*;
import java.lang.reflect.*;
import java.util.List;

/** Temporary metadata-only diagnostic hook; never changes a request or surface. */
public final class SessionTrace {
  private static Object value(Object v) throws Exception {
    if (v == null) return JSONObject.NULL;
    if (v.getClass().isArray()) {
      JSONArray a = new JSONArray();
      for(int i=0;i<Array.getLength(v);i++) a.put(value(Array.get(v,i)));
      return a;
    }
    if (v instanceof Number || v instanceof Boolean || v instanceof String) return v;
    return v.toString();
  }
  private static Object surfaceInfo(String method, Surface surface) {
    try {
      Class<?> cls = Class.forName("android.hardware.camera2.utils.SurfaceUtils");
      return value(cls.getDeclaredMethod(method, Surface.class).invoke(null,surface));
    } catch(Throwable e) { return e.toString(); }
  }
  @SuppressWarnings({"rawtypes","unchecked"})
  public static void record(CaptureRequest request, List<OutputConfiguration> outputs, int mode) {
    try {
      File folder = new File("/data/user/0/com.android.camera/files/session-trace");
      folder.mkdirs();
      String name = Long.toString(System.currentTimeMillis());
      JSONObject root = new JSONObject().put("mode",mode);
      JSONArray keys = new JSONArray();
      for(CaptureRequest.Key key : request.getKeys()) {
        Object v = request.get(key);
        keys.put(new JSONObject().put("name",key.getName())
            .put("class",v == null ? "null" : v.getClass().getName()).put("value",value(v)));
      }
      root.put("keys",keys);
      JSONArray streams = new JSONArray();
      for(OutputConfiguration output : outputs) {
        JSONObject row = new JSONObject().put("description",output.toString());
        for(String method : new String[]{"getPhysicalCameraId","getStreamUseCase","getDynamicRangeProfile","getTimestampBase","getSurfaceGroupId"}) {
          try { row.put(method,value(output.getClass().getMethod(method).invoke(output))); }
          catch(Throwable e) { row.put(method,e.toString()); }
        }
        for(String method : new String[]{"getSurfaceSize","getSurfaceFormat","getSurfaceDataspace","getSurfaceUsage"})
          row.put(method,surfaceInfo(method,output.getSurface()));
        streams.put(row);
      }
      root.put("outputs",streams);
      try(FileOutputStream file = new FileOutputStream(new File(folder,name+".json"))) {
        file.write(root.toString(2).getBytes("UTF-8"));
      }
      try {
        Object metadata = request.getClass().getMethod("getNativeCopy").invoke(request);
        Parcel parcel = Parcel.obtain();
        try {
          metadata.getClass().getMethod("writeToParcel",Parcel.class,int.class).invoke(metadata,parcel,0);
          try(FileOutputStream file = new FileOutputStream(new File(folder,name+".metadata"))) { file.write(parcel.marshall()); }
        } finally { parcel.recycle(); }
      } catch(Throwable e) { Log.e("OdinSessionTrace","metadata parcel",e); }
      Log.i("OdinSessionTrace","saved "+name+" mode="+mode+" streams="+outputs.size());
    } catch(Throwable e) { Log.e("OdinSessionTrace","record failed",e); }
  }
}
