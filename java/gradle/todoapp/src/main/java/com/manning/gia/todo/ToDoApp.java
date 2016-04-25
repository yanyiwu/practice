package com.manning.gia.todo;

import com.manning.gia.todo.repository.InMemoryToDoRepository;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

public class ToDoApp {
    private static Logger logger = LogManager.getLogger(ToDoApp.class);

    public static void main(String[] args) {
        InMemoryToDoRepository repo = new InMemoryToDoRepository();
        System.out.println("hello todoapp");
        logger.debug("hello debug log4j");
        logger.info("hello info log4j");
        logger.error("hello error log4j");
        logger.fatal("hello fatal log4j");
        logger.error("hello error log4j");
    }
}
