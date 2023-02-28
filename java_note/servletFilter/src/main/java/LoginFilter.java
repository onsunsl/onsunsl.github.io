import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;


@WebFilter(urlPatterns = "/*")
public class LoginFilter implements Filter

{
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        System.out.println("初始化");
    }

    @Override
    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain filterChain) throws IOException, ServletException {
        System.out.println("过滤执行");
        HttpServletRequest request = (HttpServletRequest)req;
        String user = request.getParameter("user");
        if(user != null)
        {
            filterChain.doFilter(req, resp);
            System.out.println("登录用户：" + user);
        }
        else{
            System.out.println("请登录");
            HttpServletResponse   response = (HttpServletResponse) resp;
            response.setContentType("text/html");
            response.getWriter().write("<h1>Please login!</h1>");
        }
    }

    @Override
    public void destroy() {
        System.out.println("销毁");

    }

}