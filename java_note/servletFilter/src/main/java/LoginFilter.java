import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 *  登录过滤器实现未登录拦截
 *  根据命中的url 执行过滤器
 */
@WebFilter(urlPatterns = "/*")
public class LoginFilter implements Filter {
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        System.out.println("初始化");
    }

    @Override
    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain filterChain) throws IOException, ServletException {
        System.out.println("过滤执行");
        HttpServletRequest request = (HttpServletRequest) req;
        String user = request.getParameter("user");

        // 模拟登录
        if (user != null) {
            // 通过过滤器转发到Servlet层
            filterChain.doFilter(req, resp);
            System.out.println("登录用户：" + user);
        } else {
            // 被过滤了
            System.out.println("请登录");
            HttpServletResponse response = (HttpServletResponse) resp;
            response.setContentType("text/html");
            response.getWriter().write("<h1>Please login!</h1>");
        }
    }

    @Override
    public void destroy() {
        System.out.println("销毁");

    }

}