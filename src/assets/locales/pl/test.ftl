test-message = { $tasks_count ->
    [0]     Witaj, { $user_name }! Nie masz żadnych zadań.
    [one]   Witaj, { $user_name }! Masz { $tasks_count } zadanie.
    *[other] Witaj, { $user_name }! Masz { $tasks_count } zadań.
}
