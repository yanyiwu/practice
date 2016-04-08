package com.manning.gia.todo.repository;

import com.manning.gia.todo.model.ToDoItem;
import java.util.List;

public interface ToDoRepository {
    List<ToDoItem> findAll();
    ToDoItem findById(Long id);
    Long insert(ToDoItem item);
    void update(ToDoItem item);
    void delete(ToDoItem item);
}
