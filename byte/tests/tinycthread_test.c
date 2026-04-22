#include <stdlib.h>
#include <stdio.h>

#include "../cruntime/tinycthread/tinycthread.c"


#define NUM_THREADS 100

typedef struct {
    int a;
    int b;
    int thread_index;
} multiply_thread;

int thread(void* arg) {
    multiply_thread data = *(multiply_thread*)arg;
    free(arg);
    
    printf("Thread Index = %d, a = %d, b = %d, Result = %d\n", data.thread_index, data.a, data.b, data.a * data.b);
    return 0;
}

int main(void) {
    for (int i = 0; i < NUM_THREADS; i++) {
        multiply_thread* arg = (multiply_thread*)malloc(sizeof(multiply_thread));
        if (arg == NULL) {
            fputs("out of memory", stderr);
            return 1;
        }
        
        arg->a = rand() % 100;
        arg->b = rand() % 100;
        arg->thread_index = i;
        thrd_t t;
        if (thrd_create(&t, thread, arg) != thrd_success) {
            fputs("failed to start thread", stderr);
            free(arg);
            return 1;
        }
        
        thrd_detach(t);
    }
    
    thrd_sleep(&(struct timespec){1, 0}, NULL);
    return 0;
}
