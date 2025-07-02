package com.pasit.crudapp.repository;

import com.pasit.crudapp.entity.Person;

import java.util.List;

public interface PersonDAO {
    //Insert
    void save(Person person);
    //Delete
    void delete(Integer id);
    //Get by ID
    Person get(Integer id);
    //Get all Data Query
    List<Person> getAll();
    //Update data
    void update(Person person);
}
