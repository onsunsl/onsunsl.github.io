package com.demo.dao;


import com.demo.dto.Person;

import java.util.List;

/**
 * Person 对象增删改查操作接口
 */
public interface PersonDao {
    Integer createTable();

    Integer dropTable();

    List<Person> selectAll();

    Person selectById(Integer id);

    Integer deleteById(Integer id);

    Integer update(Person person);

    Integer insert(Person person);

}

