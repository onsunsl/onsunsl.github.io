package com.example.springbootopenapi;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.Contact;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@Configuration
@EnableSwagger2
public class SwaggerConfig {

    @Bean
    public Docket createRestApi() {
        Docket docket = new Docket(DocumentationType.SWAGGER_2);

        return docket.apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.example.springbootopenapi"))
                .paths(PathSelectors.any())
                .build();

    }

    private ApiInfo apiInfo()
    {
        ApiInfoBuilder builder = new ApiInfoBuilder();
        return builder.title("API 文档")
                .description("这个是spring boot open api 自动生成的接口文档信息")
                .version("V1")
                .contact(new Contact("Hello", "https://www.hello.com", ""))
                .license("GPL")
                .licenseUrl("https://www.hello.com")
                .build();
    }
}
