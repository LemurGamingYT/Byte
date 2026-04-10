#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

#include "../cruntime/tinycthread/tinycthread.c"


#define MAX_QUEUE 1024

typedef struct {
    void (*function)(void*);
    void* arg;
} job_t;

typedef struct {
    job_t queue[MAX_QUEUE];
    int head;
    int tail;
    int count;
    
    mtx_t mutex;
    cnd_t cond;
    
    bool stop;
} thread_pool_t;


void do_work(void* arg) {
    int index = *(int*)arg;
    printf("Processing job: %d\n", index);
    free(arg);
}

int worker(void* arg) {
    thread_pool_t pool = *(thread_pool_t*)arg;
    while (true) {
        mtx_lock(&pool.mutex);
        while (pool.count == 0 && !pool.stop) {
            cnd_wait(&pool.cond, &pool.mutex);
        }
        
        if (pool.stop) {
            mtx_unlock(&pool.mutex);
            break;
        }
        
        job_t job = pool.queue[pool.head];
        pool.head = (pool.head + 1) % MAX_QUEUE;
        pool.count--;
        
        mtx_unlock(&pool.mutex);
        job.function(job.arg);
    }
    
    return 0;
}

void thread_pool_init(thread_pool_t* pool, int num_workers) {
    pool->head = pool->tail = pool->count = 0;
    pool->stop = false;
    
    mtx_init(&pool->mutex, mtx_plain);
    cnd_init(&pool->cond);
    
    for (int i = 0; i < num_workers; i++) {
        thrd_t t;
        thrd_create(&t, worker, pool);
        thrd_detach(t);
    }
}

void thread_pool_add_job(thread_pool_t* pool, void (*function)(void*), void* arg) {
    mtx_lock(&pool->mutex);
    if (pool->count == MAX_QUEUE) {
        puts("Queue full");
        mtx_unlock(&pool->mutex);
        return;
    }
    
    pool->queue[pool->tail].function = function;
    pool->queue[pool->tail].arg = arg;
    pool->tail = (pool->tail + 1) % MAX_QUEUE;
    pool->count++;
    
    cnd_signal(&pool->cond);
    mtx_unlock(&pool->mutex);
}

void thread_pool_destroy(thread_pool_t* pool) {
    mtx_lock(&pool->mutex);
    pool->stop = true;
    cnd_broadcast(&pool->cond);
    mtx_unlock(&pool->mutex);
}


int main(void) {
    thread_pool_t pool;
    thread_pool_init(&pool, 4);
    for (int i = 0; i < 1000; i++) {
        int* arg = (int*)malloc(sizeof(int));
        *arg = i;
        thread_pool_add_job(&pool, do_work, arg);
    }
    
    thrd_sleep(&(struct timespec){2}, NULL);
    thread_pool_destroy(&pool);
    return 0;
}
