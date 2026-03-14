test-message = { $tasks_count ->
    [0]     Вітаю, { $user_name }! У вас немає завдань.
    [one]   Вітаю, { $user_name }! У вас { $tasks_count } завдання.
    [few]   Вітаю, { $user_name }! У вас { $tasks_count } завдання.
    [many]  Вітаю, { $user_name }! У вас { $tasks_count } завдань.
   *[other] Вітаю, { $user_name }! У вас { $tasks_count } завдань.
}