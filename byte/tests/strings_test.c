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
    fprintf(stderr, "error: %s", message);
    exit(EXIT_FAILURE);
}

void string_destroy(string s) {
    if (!s.is_allocated) return;
    free(s.ptr);
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

void print(string s) {
    printf("%.*s\n", s.length, s.ptr);
}

string input(void) {
    char buf[512];
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        error("stream error");
    }
    
    int newline_pos = strcspn(buf, "\n");
    return (string){buf, newline_pos, false};
}

int main(void) {
    return 0;
}
