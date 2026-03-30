#include <stdio.h>


int main(void) {
    const char* str = "Hello world\n";
    printf("%.*s\n", 5, str);
    return 0;
}
