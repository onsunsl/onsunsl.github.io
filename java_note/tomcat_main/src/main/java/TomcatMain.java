import org.apache.catalina.Context;
import org.apache.catalina.WebResourceRoot;
import org.apache.catalina.startup.Tomcat;
import org.apache.catalina.webresources.DirResourceSet;
import org.apache.catalina.webresources.StandardRoot;

import java.io.File;

public class TomcatMain {
    public static void main(String[] args)  throws Exception{
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(8080);
        tomcat.getConnector();

        String appPath = new File("src/main/webapp").getAbsolutePath();
        String appClassPath = new File("target/classes").getAbsolutePath();

        Context context = tomcat.addWebapp("", appPath);
        WebResourceRoot resourceRoot = new StandardRoot(context);

        DirResourceSet resourceSet = new DirResourceSet(resourceRoot, "/WEB-INF/classes", appClassPath, "/");
        resourceRoot.addPreResources(resourceSet);

        context.setResources(resourceRoot);
        tomcat.start();
        tomcat.getServer().await();
    }
}
