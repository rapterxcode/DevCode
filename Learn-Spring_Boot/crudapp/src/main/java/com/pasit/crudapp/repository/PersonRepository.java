package com.pasit.crudapp.repository;

import com.pasit.crudapp.entity.Person;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.lang.reflect.Type;
import java.util.List;

@Repository
public class PersonRepository implements PersonDAO {

    private EntityManager entityManager;

    @Autowired
    public PersonRepository(EntityManager entityManager) {
        this.entityManager = entityManager;
    }
//Insert
    @Override
    @Transactional
    public void save(Person person) {
        entityManager.persist(person);
    }
//Delete
    @Override
    @Transactional
    public void delete(Integer id) {
        Person person = entityManager.find(Person.class,id);
        System.out.println(person);
        entityManager.remove(person);
    }
//Get by id
    @Override
    public Person get(Integer id) {
        return entityManager.find(Person.class,id);
    }
//Get all data
    @Override
    public List<Person> getAll() {
        TypedQuery<Person> query = entityManager.createQuery("FROM Person",Person.class);
        return query.getResultList();
    }
//Update
    @Override
    @Transactional
    public void update(Person person) {
        entityManager.merge(person);
    }


}
