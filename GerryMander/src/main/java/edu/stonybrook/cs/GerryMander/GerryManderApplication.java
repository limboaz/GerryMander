package edu.stonybrook.cs.GerryMander;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class GerryManderApplication {

	public static void main(String[] args) {
		SpringApplication.run(GerryManderApplication.class, args);
	}

}
