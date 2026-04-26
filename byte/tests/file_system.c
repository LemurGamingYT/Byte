#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>


typedef struct {
    const char* path;
} File;

#define PERMISSION_DENIED_ERROR 13
#define FILE_DOES_NOT_EXIST 2


void error(const char* message) {
    fprintf(stderr, "error: %s\n", message);
    exit(EXIT_FAILURE);
}

void handle_file_error(errno_t error_code) {
    switch (error_code) {
    case EXIT_SUCCESS:
        break;
    case PERMISSION_DENIED_ERROR:
        error("permission denied");
        break;
    case FILE_DOES_NOT_EXIST:
        error("no such file or directory");
        break;
    default:
        printf("New Error Code: %d\n", error_code);
        perror("file error");
    }
}

File File_new(const char* path) {
    return (File){path};
}

void File_write(const File* file, const char* content) {
    FILE* fp;
    errno_t error_code = fopen_s(&fp, file->path, "w");
    handle_file_error(error_code);
    
    fprintf(fp, "%s", content);
    fclose(fp);
}

char* File_contents(const File* file) {
    FILE* fp;
    errno_t error_code = fopen_s(&fp, file->path, "r");
    handle_file_error(error_code);
    
    fseek(fp, 0, SEEK_END);
    long length = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    
    char* buf = (char*)malloc(length + 1);
    if (buf == NULL) {
        fclose(fp);
        error("out of memory");
    }
    
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
    File file = File_new("byte");
    char* contents = File_contents(&file);
    puts(contents);
    
    free(contents);
    return 0;
}
