#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


typedef struct {
    char* ptr;
    int length;
} string;


void error(const char* message) {
    fprintf(stderr, "error: %s", message);
    exit(EXIT_FAILURE);
}

void string_destroy(string s) {
    free(s.ptr);
}

string string_new(const char* ptr, int length) {
    char* ptr_copy = (char*)malloc(length);
    if (ptr_copy == NULL) error("out of memory");
    
    memcpy(ptr_copy, ptr, length);
    return (string){ptr_copy, length};
}

string string_new_length(int length) {
    char* ptr = (char*)malloc(length);
    if (ptr == NULL) error("out of memory");
    
    memset(ptr, ' ', length);
    return (string){ptr, length};
}

string add_strings(string a, string b) {
    int length = a.length + b.length;
    char* ptr = (char*)malloc(length);
    if (ptr == NULL) error("out of memory");
    
    memcpy(ptr, a.ptr, a.length);
    memcpy(ptr + a.length, b.ptr, b.length);
    return (string){ptr, length};
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
    printf("%.*s", s.length, s.ptr);
}


int main(void) {
    string a = string_new_length(2);
    string b = string_new_length(2);
    string c = add_strings(a, b);
    printf("=%d, !=%d", eq_strings(a, b), neq_strings(a, b));
    print(c);
    string_destroy(a);
    string_destroy(b);
    string_destroy(c);
    return 0;
}
