package edu.stonybrook.cs.GerryMander;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = {"edu.stonybrook.cs.GerryMander.Model"})
public class GerryManderApplication {

	public static void main(String[] args) {
		SpringApplication.run(GerryManderApplication.class, args);
	}

}
