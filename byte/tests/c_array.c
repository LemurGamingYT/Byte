#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>

#include "../cruntime/asprintf.c"


#define ARRAY_CAPACITY 4

typedef struct {
    int* elements;
    int length;
} int_array;


char* int_to_string(int i) {
    static char buf[16];
    snprintf(buf, sizeof(buf), "%d", i);
    return buf;
}

int_array array_new(void) {
    int* elements = (int*)malloc(sizeof(int) * ARRAY_CAPACITY);
    return (int_array){elements, 0};
}

void array_destroy(int_array* arr) {
    free(arr->elements);
    arr->elements = NULL;
    arr->length = 0;
}

void array_add(int_array* arr, int x) {
    assert(arr->length < ARRAY_CAPACITY);

    arr->elements[arr->length++] = x;
}

int array_get(const int_array* arr, int idx) {
    if (idx < 0)
        idx = arr->length + idx;

    assert(idx < arr->length);
    return arr->elements[idx];
}

char* array_to_string(const int_array* arr) {
    const int static_size = 2; // '[' and ']'
    int fmt_size = static_size;
    if (arr->length != 0) {
        int length_size = arr->length * 2; // each element is '%s'
        int num_commas = arr->length - 1; // each element (except the last one) has a comma
        int comma_size = num_commas * 2; // each comma is ', ' (2 characters)
        int elements_size = length_size + comma_size;
        fmt_size += elements_size;
    }

    printf("%d\n", fmt_size);
    char* fmt = (char*)malloc(fmt_size + 1);
    assert(fmt != NULL);

    int fmt_idx = 0;
    memcpy(fmt, "[", 1);
    fmt_idx++;
    
    for (int i = 0; i < arr->length; i++) {
        memcpy(fmt + fmt_idx, "%s", 2);
        fmt_idx += 2;

        if (i < arr->length - 1) {
            memcpy(fmt + fmt_idx, ", ", 2);
            fmt_idx += 2;
        }
    }

    memcpy(fmt + fmt_idx, "]", 1);
    fmt_idx++;

    fmt[fmt_size] = '\0';
    return fmt;
}

int main(void) {
    int_array arr = array_new();
    array_add(&arr, 1);
    array_add(&arr, 2);

    char* buf = array_to_string(&arr);
    printf("%s\n", buf);
    free(buf);
    
    array_destroy(&arr);
    return 0;
}
