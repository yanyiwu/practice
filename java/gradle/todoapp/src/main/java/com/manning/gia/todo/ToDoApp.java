package com.manning.gia.todo;

import com.manning.gia.todo.repository.InMemoryToDoRepository;

public class ToDoApp {
    public static void main(String[] args) {
        InMemoryToDoRepository repo = new InMemoryToDoRepository();
        System.out.println("todoapp");
    }
}
