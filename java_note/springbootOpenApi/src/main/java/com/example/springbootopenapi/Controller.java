package com.example.springbootopenapi;

import io.swagger.annotations.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;


@RestController
@Api(value = "知识追寻者文档API")
public class Controller {

    @ApiOperation(value = "这个是一个结款")
    @GetMapping("/hello")
    public String HelloApi()
    {
        return "";
    }

    @ApiOperation(value = "获取用")
    @ApiResponse(code=200, message = "获取用户成功")
    @GetMapping("/getUser")
    public ResponseEntity<User> getUser()
    {
        User user = new User();
        user.setAge(10);
        user.setEmail("hello@world.com");
        user.setHobby("打球");
        user.setName("小李");
        return ResponseEntity.ok(user);
    }


    // 方法注释
    @ApiOperation(value = "跟据用户编号获取用户")
    // 响应信息
    @ApiResponses({@ApiResponse(code = 200,message = "获取用户列表成功") ,@ApiResponse(code = 204,message = "没有内容")})
    // 参数信息
    @ApiImplicitParam(name = "id", value = "用户编号", dataType = "int",required = true, paramType = "path")
    @GetMapping("user/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id){
        User user = new User();
        user.setAge(10);
        user.setEmail("hello@world.com");
        user.setHobby("打球");
        user.setName("小李");
        return ResponseEntity.ok(user);
    }




}
