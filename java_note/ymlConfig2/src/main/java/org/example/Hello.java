package org.example;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.text.MessageFormat;


@RestController
@SpringBootApplication
public class Hello {

    @Value("${spring.application.name}")
    private String name;

    @Value("${spring.profiles.active}")
    private String env;

    @RequestMapping("hello")
    String hello()
    {

        return MessageFormat.format("{0} {1}环境, 当前是：{2}", "hello", this.name, this.env);
    }

    public static void main(String[] args) {
        SpringApplication.run(Hello.class, args);
    }
}
