package com.pasit.crudmyapi.controllers;

import com.pasit.crudmyapi.entity.User;
import com.pasit.crudmyapi.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
//Rest Controller
@RestController
@RequestMapping("/api")
public class UserController {
    //Import UserService Use in UserController
    private UserService userService;
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    //Save Data to DB Method
    @PostMapping("/users")
    public User addUser(@RequestBody User user){
        user.setId(0);
        return userService.save(user);
    }
    //Get All Data
    @GetMapping("/users")
    public List<User> getAllUser(){
        return userService.findAll();
    }
    //Get Data by ID
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable int id){
        User myUser = userService.findById(id);
        if (myUser==null){
            throw new RuntimeException("Not Found User "+id);
        }
        return myUser;
    }
    //Delete Data by ID
    @DeleteMapping("/users/{id}")
    public String deleteUser(@PathVariable int id){
        User myUser = userService.findById(id);
        if (myUser==null){
            throw new RuntimeException("Not Found User "+id);
        }
        userService.deleteById(id);
        return "Delete User "+id+" Complate";
    }
    //Update Data
    @PutMapping("users")
    public User updateUser(@RequestBody User user){
        return userService.save(user);
    }
    /* @GetMapping("/users")
    public List getUsers(){
        List<User> data = new ArrayList<User>();
        data.add(new User("Pasit", "Chatcharoenkit"));
        data.add(new User("Test1", "EndTest1"));
        data.add(new User("Test2", "EndTest2"));
        return data;
    }

    @GetMapping("/about")
    public String getAbout(){
        return "About Test";
    }

    @GetMapping("/addresses")
    public String getAddresses(){
        return "Address Test";
    }

    @GetMapping("/jobs")
    public String getJobs(){
        return "Programmer";
    }

    */
}
