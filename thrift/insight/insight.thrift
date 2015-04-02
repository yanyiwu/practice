struct Person {
    1: string name,
    2: i32 age,
    3: optional string address,
}

service Insight {
    Person Hello(1: Person person),
    Person Hi(1: Person p1, 2: Person p2),
}
