package com.example.springbootopenapi;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;


@Data
@ApiModel(description = "用户信息实体类")
public class User {

    @ApiModelProperty(value = "姓名", dataType = "String")
    private String name;

    @ApiModelProperty(value = "邮箱", dataType = "String")
    private String email;

    @ApiModelProperty(value = "爱好", dataType = "String")
    private String hobby;

    @ApiModelProperty(value = "年龄", dataType = "int")
    private int age;

}
