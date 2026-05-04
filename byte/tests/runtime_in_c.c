#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


typedef struct {
    char* ptr;
    int length;
    bool is_allocated;
} string;


void error(const char* message) {
    fprintf(stderr, "error: %s\n", message);
    exit(EXIT_FAILURE);
}

void string_destroy(string* s) {
    if (!s->is_allocated) return;
    free(s->ptr);
}

string string_new(const char* ptr, int length) {
    char* ptr_copy = (char*)malloc(length);
    if (ptr_copy == NULL) error("out of memory");
    
    memcpy(ptr_copy, ptr, length);
    return (string){ptr_copy, length, true};
}

string string_new_length(int length) {
    char* ptr = (char*)malloc(length);
    if (ptr == NULL) error("out of memory");
    
    memset(ptr, ' ', length);
    return (string){ptr, length, true};
}

string add_strings(string a, string b) {
    int length = a.length + b.length;
    char* ptr = (char*)malloc(length);
    if (ptr == NULL) error("out of memory");
    
    memcpy(ptr, a.ptr, a.length);
    memcpy(ptr + a.length, b.ptr, b.length);
    return (string){ptr, length, true};
}

bool eq_strings(string a, string b) {
    if (a.length != b.length) return false;
    return memcmp(a.ptr, b.ptr, a.length) == false;
}

bool neq_strings(string a, string b) {
    if(a.length != b.length) return true;
    return memcmp(a.ptr, b.ptr, a.length) != false;
}

int string_to_int(string s) {
    return strtol(s.ptr, NULL, 10);
}

float string_to_float(string s) {
    return strtof(s.ptr, NULL);
}

string int_to_string(int i) {
    static char buf[16];
    int written = snprintf(buf, sizeof(buf), "%d", i);
    return (string){(char*)buf, written, false};
}

void print(string s) {
    printf("%.*s\n", s.length, s.ptr);
}

int main(void) {
    string s = int_to_string(-2147483648);
    print(s);

    string len = int_to_string(s.length);
    print(len);

    string_destroy(&s);
    string_destroy(&len);
    return 0;
}
