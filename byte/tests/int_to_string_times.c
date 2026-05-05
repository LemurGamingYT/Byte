#include <windows.h>
#include <stdio.h>


#define NUM_ITERATIONS 100000000

typedef struct {
    LARGE_INTEGER frequency, counter;
} PerformanceTimer;

long long PerformanceTimer_clock(PerformanceTimer* pt) {
    QueryPerformanceCounter(&pt->counter);
    return (pt->counter.QuadPart * 1000000000LL) / pt->frequency.QuadPart;
}

int PerformanceTimer_init(PerformanceTimer* pt) {
    return QueryPerformanceCounter(&pt->frequency);
}

char* int_to_string_snprintf(int i) {
    static char buf[16];
    snprintf(buf, sizeof(buf), "%d", i);
    return buf;
}

char* int_to_string_manual(int i) {
    static char buf[16];
    char* p = buf + sizeof(buf) - 1;
    *p = '\0';

    int is_negative = i < 0;
    unsigned int v = is_negative ? -(unsigned int)i : i;

    do {
        *--p = '0' + (v % 10);
        v /= 10;
    } while (v);

    if (is_negative) {
        *--p = '-';
    }

    return buf;
}

volatile int sink;
int main(void) {
    PerformanceTimer pt;
    PerformanceTimer_init(&pt);

    for (int i = 0; i < 100000; i++) {
        static char buf[16];
        char* p = buf + sizeof(buf) - 1;
        *p = '\0';
    
        int is_negative = i < 0;
        unsigned int v = is_negative ? -(unsigned int)i : i;
    
        do {
            *--p = '0' + (v % 10);
            v /= 10;
        } while (v);
    
        if (is_negative) {
            *--p = '-';
        }

        sink += (buf + sizeof(buf) - 1) - p;
    }

    long long start = PerformanceTimer_clock(&pt);
    for (int i = 0; i < NUM_ITERATIONS; i++) {
        int_to_string_snprintf(i);
    }

    long long end = PerformanceTimer_clock(&pt);
    double avg = (double)(end - start) / NUM_ITERATIONS;
    
    printf("executed in %.2f ns\n", avg);
    return 0;
}
