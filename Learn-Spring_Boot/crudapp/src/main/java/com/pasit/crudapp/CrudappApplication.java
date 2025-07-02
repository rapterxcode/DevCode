package com.pasit.crudapp;

import com.pasit.crudapp.entity.Person;
import com.pasit.crudapp.repository.PersonDAO;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.List;

@SpringBootApplication
public class CrudappApplication {

	public static void main(String[] args) {
		SpringApplication.run(CrudappApplication.class, args);
	}

	@Bean
	public CommandLineRunner commandLineRunner(PersonDAO dao){
		return runner->{
//Call Use medtod
			//saveData(dao);
			//deleteData(dao);
			//getData(dao);
			getAllData(dao);
			//updateData(dao);
		};
	}
//Insert
	public void saveData(PersonDAO dao){
		Person obj1=new Person("phone","lastphone");
		dao.save(obj1);
		System.out.println("====================");
		System.out.println("Insert Complate");
		System.out.println("====================");
	}
//Delete
	public void deleteData(PersonDAO dao){
		int id=2;
		dao.delete(id);
		System.out.println("====================");
		System.out.println("Delete Complate");
		System.out.println("====================");
	}
//Get data with id
	public void getData(PersonDAO dao){
		int id=1;
		Person person = dao.get(id);
		System.out.println("====================");
		System.out.println("Get Data by id Complate");
		System.out.println(person);
		System.out.println("====================");

	}
//Get all data
	public void getAllData(PersonDAO dao){
		List<Person> data = dao.getAll();
		System.out.println("====================");
		for(Person person : data){
			System.out.println(person);
		}
		System.out.println("====================");
	}
//Update Data
	public void  updateData(PersonDAO dao){
		int id=4;
		Person myPerson = dao.get(id);
		myPerson.setFname("JOJO");
		myPerson.setLname("NAJA");
		dao.update(myPerson);
		System.out.println("====================");
		System.out.println(myPerson);
		System.out.println("Update Complate");
		System.out.println("====================");
	}
}
