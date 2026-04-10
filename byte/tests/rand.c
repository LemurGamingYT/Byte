#include <stdlib.h>
#include <stdio.h>
#include <time.h>


int generate_random_number(int min, int max) {
    if (min > max)
        min = max;
    
    if (min == max)
        max++;
    
    int range = max - min;
    return rand() % range + min;
}

int main(void) {
    srand(time(NULL));
    
    for (int i = 0; i < 10; i++) {
        printf("Generating random number between 5 and 20 %d\n", generate_random_number(5, 20));
    }
    
    return 0;
}
