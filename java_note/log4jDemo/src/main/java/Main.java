import org.apache.log4j.Logger;

import java.text.MessageFormat;

class Fmt
{
    public static String t(String fmt, Object ... params)
    {
        return MessageFormat.format(fmt, params);
    }
}

public class Main {


    public static void main(String[] args) {
        Logger log = Logger.getLogger("debug");
        Integer i;
        log.info(Fmt.t("hello info:{0} {1}", "123", 5683));
        log.warn("hello warning");
        log.error("hello error");
        log.fatal("hello fatal");
    }
}
