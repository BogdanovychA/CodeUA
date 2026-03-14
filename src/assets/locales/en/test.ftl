test-message = { $tasks_count ->
    [0]     Welcome, { $user_name }! You have no tasks.
    [one]   Welcome, { $user_name }! You have { $tasks_count } task.
   *[other] Welcome, { $user_name }! You have { $tasks_count } tasks.
}