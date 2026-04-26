#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>


typedef struct {
    void* data;
    bool is_freed;
    size_t size;
} Pointer;


void error(const char* message) {
    fprintf(stderr, "error: %s\n", message);
    exit(EXIT_FAILURE);
}

Pointer Pointer_new(void* data, size_t size) {
    return (Pointer){data, false, size};
}

void Pointer_free(Pointer* ptr) {
    if (ptr->is_freed) return;
    
    free(ptr->data);
    ptr->is_freed = true;
}

#define Pointer_read(T) T Pointer_read_##T(const Pointer* ptr) {\
    if (ptr->is_freed)\
        error("use after free");\
    return *(T*)ptr->data;\
}

#define Pointer_write(T) void Pointer_write_##T(Pointer* ptr, T data) {\
    if (ptr->is_freed) error("use after free");\
    *(T*)ptr->data = data;\
}

void Pointer_copy(const Pointer* ptr, Pointer* to) {
    if (ptr->is_freed || to->is_freed)
        error("use after free");
    
    if (ptr->size != to->size)
        error("pointer sizes do not match");
    
    memcpy(to->data, ptr->data, ptr->size);
}

void Pointer_zero(Pointer* ptr) {
    if (ptr->is_freed)
        error("use after free");
    
    memset(ptr->data, 0, ptr->size);
}

Pointer_write(int)
Pointer_read(int)

int main(void) {
    int* data = (int*)malloc(sizeof(int));
    if (data == NULL)
        error("out of memory");
    
    Pointer ptr = Pointer_new((void*)data, sizeof(int));
    Pointer_zero(&ptr);
    
    printf("%d\n", Pointer_read_int(&ptr));
    
    Pointer_write_int(&ptr, 5);
    
    printf("%d\n", Pointer_read_int(&ptr));
    Pointer_free(&ptr);
    return 0;
}
