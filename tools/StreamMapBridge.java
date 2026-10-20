package com.odin.compat;
import java.lang.reflect.Constructor;
public final class StreamMapBridge {
    public static Object build(Object[] original) {
        try {
            Class<?> cls = Class.forName("android.hardware.camera2.params.StreamConfigurationMap");
            Constructor<?> selected = null;
            for (Constructor<?> c : cls.getDeclaredConstructors()) {
                Class<?>[] p = c.getParameterTypes();
                if ((p.length == 15 || p.length == 18 || p.length == 21)
                        && p[p.length - 1] == boolean.class
                        && p[p.length - 2].getName().equals("android.hardware.camera2.params.ReprocessFormatsMap")) {
                    if (selected == null || p.length > selected.getParameterTypes().length) selected = c;
                }
            }
            if (selected == null) throw new NoSuchMethodException("Unsupported StreamConfigurationMap signature");
            int count = selected.getParameterTypes().length;
            Object[] args = new Object[count];
            // Keep the vendor's normal, depth, dynamic-depth and HEIC maps intact.
            System.arraycopy(original, 0, args, 0, 12);
            // JPEG-R and HEIC Ultra HDR are new framework parameters absent from this OEM app.
            // Passing null is the legacy constructor's delegation behavior.
            System.arraycopy(original, 12, args, count - 3, 3);
            selected.setAccessible(true);
            return selected.newInstance(args);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("MIUI camera Camera2 constructor compatibility failed", e);
        }
    }
}
