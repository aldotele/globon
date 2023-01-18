package util;

import java.util.regex.Pattern;

public class RegexUtil {
    public static Pattern exactIgnoreCase(String s) {
        return Pattern.compile("^" + s + "$", Pattern.CASE_INSENSITIVE);
    }
}
