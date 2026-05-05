#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "../cruntime/asprintf.c"


typedef struct {
    int x, y;
} Vector2;

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

void print(string s) {
    printf("%.*s\n", s.length, s.ptr);
}

string int_to_string(int i) {
    static char buf[16];
    int written = snprintf(buf, sizeof(buf), "%d", i);
    return (string){buf, written, false};
}

string Vector2_to_string(Vector2 vec) {
    string x_str = int_to_string(vec.x);
    string y_str = int_to_string(vec.y);
    
    char* buf = NULL;
    int written = asprintf(&buf, "Vector2(x=%.*s, y=%.*s)", x_str.length, x_str.ptr, y_str.length, y_str.ptr);
    return (string){buf, written, true};
}

int main(void) {
    Vector2 pos = {100, 100};
    string to_string = Vector2_to_string(pos);
    print(to_string);
    string_destroy(&to_string);
    return 0;
}
