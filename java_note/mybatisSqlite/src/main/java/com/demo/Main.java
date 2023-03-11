package com.demo;


import com.demo.dao.PersonDao;
import com.demo.dao.impl.PersonDaoImpl;
import com.demo.dto.Person;


import java.io.IOException;
import java.util.List;


public class Main {

    public static void main(String[] args) throws IOException {
        PersonDao personDao = new PersonDaoImpl();

        // 建表
        personDao.dropTable();
        personDao.createTable();


        // 插入数据
        personDao.insert(new Person("曹操", 23));
        personDao.insert(new Person("刘备", 24));
        personDao.insert(new Person("孙权", 21));


        // 删除
        Integer deleteResult = personDao.deleteById(1);
        System.out.println(deleteResult);


        // 查询单个
        Person person = personDao.selectById(2);
        System.out.println(person);


        // 更新
        person.setAge(25);
        Integer updateResult = personDao.update(person);
        System.out.println(updateResult);


        // 查询所有
        List<Person> list = personDao.selectAll();
        for(Person p: list){
            System.out.println(p);
        }
    }
}


