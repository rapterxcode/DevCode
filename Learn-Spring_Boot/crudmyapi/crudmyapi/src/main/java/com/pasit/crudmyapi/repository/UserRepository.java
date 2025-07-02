package com.pasit.crudmyapi.repository;

import com.pasit.crudmyapi.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
//Spring Data JPA Interface
public interface UserRepository extends JpaRepository<User,Integer> {
}
