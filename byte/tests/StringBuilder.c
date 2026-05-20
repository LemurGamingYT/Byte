#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>


typedef struct {
    char* buf;
    int length, capacity;
} StringBuilder;


StringBuilder StringBuilder_new(int capacity) {
    char* buf = (char*)malloc(capacity);
    assert(buf != NULL);
    
    return (StringBuilder){buf, 0, capacity};
}

void StringBuilder_destroy(StringBuilder* sb) {
    free(sb->buf);
    sb->buf = NULL;
    sb->length = 0;
    sb->capacity = 0;
}

void StringBuilder_add(StringBuilder* sb, const char* value) {
    int len = strlen(value);
    if (sb->length + len >= sb->capacity) {
        sb->capacity *= 2;
        sb->buf = (char*)realloc(sb->buf, sb->capacity);
        assert(sb->buf != NULL);
    }

    memcpy(sb->buf + sb->length, value, len);
    sb->length += len;
}

char* StringBuilder_str(const StringBuilder* sb) {
    char* buf = (char*)malloc(sb->length + 1);
    assert(buf != NULL);

    memcpy(buf, sb->buf, sb->length);
    buf[sb->length] = '\0';
    return buf;
}

int main(void) {
    StringBuilder sb = StringBuilder_new(25);
    StringBuilder_add(&sb, "Hello ");
    StringBuilder_add(&sb, "World ");
    StringBuilder_add(&sb, "My text ");
    StringBuilder_add(&sb, "Add some more text");

    char* buf = StringBuilder_str(&sb);
    printf("%s\n", buf);
    free(buf);

    StringBuilder_destroy(&sb);
    return 0;
}
