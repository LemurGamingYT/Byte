#include <stdbool.h>
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>


typedef struct {
    const char* path;
} File;

#define PERMISSION_DENIED_ERROR 13
#define FILE_DOES_NOT_EXIST 2


File File_new(const char* path) {
    return (File){path};
}

void File_write(const File* file, const char* content) {
    FILE* fp;
    errno_t error_code = fopen_s(&fp, file->path, "w");
    assert(error_code == EXIT_SUCCESS);
    
    fprintf(fp, "%s", content);
    fclose(fp);
}

char* File_contents(const File* file) {
    FILE* fp;
    errno_t error_code = fopen_s(&fp, file->path, "r");
    assert(error_code == EXIT_SUCCESS);
    
    fseek(fp, 0, SEEK_END);
    long length = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    
    char* buf = (char*)malloc(length + 1);
    assert(buf != NULL);
    
    fread(buf, 1, length, fp);
    buf[length] = '\0';
    
    fclose(fp);
    return buf;
}

bool File_exists(const File* file) {
    FILE* fp;
    errno_t error_code = fopen_s(&fp, file->path, "r");
    switch (error_code) {
    case EXIT_SUCCESS:
    case PERMISSION_DENIED_ERROR:
        fclose(fp);
        return true;
    default:
        fclose(fp);
        return false;
    }
}


int main(void) {
    File file = File_new("byte/tests/file_system.txt");
    File_write(&file, "Hello, World");
    char* contents = File_contents(&file);
    puts(contents);
    
    free(contents);
    return 0;
}
