package com.pasit.crudmyapi.services;

import com.pasit.crudmyapi.entity.User;
import com.pasit.crudmyapi.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

//Import UserService Interface for Use in Service
@Service
public class UserServiceAction implements UserService{

    //Import UserRepository for Use in Service
    private UserRepository userRepository;
    @Autowired
    public UserServiceAction(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    //Call Use Repository Interface name save(entiry name user)
    @Override
    public User save(User user) {
        return userRepository.save(user);
    }
    //Call User Replisitory Interface name findAll method List
    @Override
    public List<User> findAll() {
        return userRepository.findAll();
    }
    //Call User Repository Interface name findById
    @Override
    public User findById(Integer id) {
        //Call userRepository from User
        Optional<User> result = userRepository.findById(id);
        User data=null;
        if (result.isPresent()){
            data=result.get();
        }else {
            throw new RuntimeException("Not Found User "+id);
        }
        return data;
    }
    //Call deleteById from UserService
    @Override
    public void deleteById(Integer id) {
        userRepository.deleteById(id);
    }
}
