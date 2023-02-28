import org.apache.catalina.Context;
import org.apache.catalina.WebResourceRoot;
import org.apache.catalina.startup.Tomcat;
import org.apache.catalina.webresources.DirResourceSet;
import org.apache.catalina.webresources.StandardRoot;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.IOException;

@WebServlet(urlPatterns = "/")
public class TomcatMain extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String user = req.getParameter("user");
        resp.getWriter().write("hello: " + user);
    }

    public static void main(String[] args) throws Exception{
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(8080);
        tomcat.getConnector();

        Context context = tomcat.addWebapp("", new File("src/main/webapp").getAbsolutePath());
        WebResourceRoot resourceRoot = new StandardRoot(context);

        resourceRoot.addPreResources(
                new DirResourceSet(resourceRoot, "/WEB-INF/classes", new File("target/classes").getAbsolutePath(), "/")
        );

        context.setResources(resourceRoot);
        tomcat.start();
        tomcat.getServer().await();
    }
}