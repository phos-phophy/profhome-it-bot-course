#include <queue>


struct SCHEDULER {
    int working_thread;
    int timeslice;
    int current_time;
    std::queue<int> waiting_threads;
} scheduler;


/**
 * Функция будет вызвана перед каждым тестом, если вы
 * используете глобальные и/или статические переменные
 * не полагайтесь на то, что они заполнены 0 - в них
 * могут храниться значения оставшиеся от предыдущих
 * тестов.
 *
 * timeslice - квант времени, который нужно использовать.
 * Поток смещается с CPU, если пока он занимал CPU функция
 * timer_tick была вызвана timeslice раз.
 **/
void scheduler_setup(int timeslice)
{
    scheduler.timeslice = timeslice;
    scheduler.working_thread = -1;
    scheduler.current_time = 0;

    std::queue<int> empty_queue;
    std::swap(scheduler.waiting_threads, empty_queue);
}

/**
 * Функция вызывается, когда создается новый поток управления.
 * thread_id - идентификатор этого потока и гарантируется, что
 * никакие два потока не могут иметь одинаковый идентификатор.
 **/
void new_thread(int thread_id)
{
    if (scheduler.working_thread == -1) {
        scheduler.working_thread = thread_id;
        scheduler.current_time = 0;
    } else
        scheduler.waiting_threads.push(thread_id);
}

/**
 * Функция вызывается, когда поток, исполняющийся на CPU,
 * завершается. Завершится может только поток, который сейчас
 * исполняется, поэтому thread_id не передается. CPU должен
 * быть отдан другому потоку, если есть активный
 * (незаблокированный и незавершившийся) поток.
 **/
void exit_thread()
{
    scheduler.working_thread = -1;
    if (!scheduler.waiting_threads.empty()) {
        scheduler.working_thread = scheduler.waiting_threads.front();
        scheduler.waiting_threads.pop();
        scheduler.current_time = 0;
    }
}

/**
 * Функция вызывается, когда поток, исполняющийся на CPU,
 * блокируется. Заблокироваться может только поток, который
 * сейчас исполняется, поэтому thread_id не передается. CPU
 * должен быть отдан другому активному потоку, если таковой
 * имеется.
 **/
void block_thread()
{
    exit_thread();
}

/**
 * Функция вызывается, когда один из заблокированных потоков
 * разблокируется. Гарантируется, что thread_id - идентификатор
 * ранее заблокированного потока.
 **/
void wake_thread(int thread_id)
{
    new_thread(thread_id);
}

/**
 * Ваш таймер. Вызывается каждый раз, когда проходит единица
 * времени.
 **/
void timer_tick()
{
    if (++scheduler.current_time == scheduler.timeslice && scheduler.working_thread != -1) {
        scheduler.waiting_threads.push(scheduler.working_thread);
        scheduler.working_thread = -1;
    }

    if (scheduler.working_thread == -1 && !scheduler.waiting_threads.empty()) {
        scheduler.working_thread = scheduler.waiting_threads.front();
        scheduler.waiting_threads.pop();
        scheduler.current_time = 0;
    }
}

/**
 * Функция должна возвращать идентификатор потока, который в
 * данный момент занимает CPU, или -1 если такого потока нет.
 * Единственная ситуация, когда функция может вернуть -1, это
 * когда нет ни одного активного потока (все созданные потоки
 * либо уже завершены, либо заблокированы).
 **/
int current_thread()
{
    return scheduler.working_thread;
}