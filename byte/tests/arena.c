#include <stdlib.h>
#include <stdint.h>
#include <stdarg.h>
#include <assert.h>
#include <stdio.h>


#define ARENA_REGION_DEFAULT_CAPACITY (8*1024)

typedef struct Region Region;

struct Region {
    Region* next;
    size_t count, capacity;
    uintptr_t data[];
};

typedef struct {
    Region* begin, *end;
} Arena;


Region* new_region(size_t capacity) {
    size_t size_bytes = sizeof(Region) + sizeof(uintptr_t) * capacity;
    Region* r = (Region*)malloc(size_bytes);
    assert(r != NULL);
    
    r->next = NULL;
    r->count = 0;
    r->capacity = capacity;
    return r;
}

void free_region(Region* region) {
    free(region);
}

void* Arena_alloc(Arena* a, size_t size_bytes) {
    size_t size = (size_bytes + sizeof(uintptr_t) - 1) / sizeof(uintptr_t);
    if (a->end == NULL) {
        assert(a->begin == NULL);
        size_t capacity = ARENA_REGION_DEFAULT_CAPACITY;
        if (capacity < size) capacity = size;
        a->end = new_region(capacity);
        a->begin = a->end;
    }

    while (a->end->count + size > a->end->capacity && a->end->next != NULL) {
        a->end = a->end->next;
    }

    if (a->end->count + size > a->end->capacity) {
        assert(a->end->next == NULL);
        size_t capacity = ARENA_REGION_DEFAULT_CAPACITY;
        if (capacity < size) capacity = size;
        a->end->next = new_region(capacity);
        a->end = a->end->next;
    }

    void* result = &a->end->data[a->end->count];
    a->end->count += size;
    return result;
}

void Arena_reset(Arena* a) {
    for (Region* r = a->begin; r != NULL; r = r->next) {
        r->count = 0;
    }

    a->end = a->begin;
}

void Arena_free(Arena* a) {
    Region* r = a->begin;
    while (r) {
        Region* temp = r;
        r = r->next;
        free_region(temp);
    }

    a->begin = NULL;
    a->end = NULL;
}

int main(void) {
    Arena a = { .begin = NULL, .end = NULL };
    int* data = (int*)Arena_alloc(&a, sizeof(int));
    *data = 10;
    printf("%d\n", *data);
    
    Arena_free(&a);
    return 0;
}
