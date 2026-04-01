#include <stdbool.h>
#include <string.h>
#include <stdio.h>


int main(void) {
    char buf[512];
    if (!fgets(buf, 512, stdin)) {
        fputs("Error getting user input", stderr);
        return 1;
    }
    
    buf[strcspn(buf, "\n")] = 0;
    puts(buf);
    return 0;
}
