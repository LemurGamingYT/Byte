#include <stdio.h>


FILE* openfd(int fd, const char* mode) {
#if _WIN32
    return __acrt_iob_func(fd);
#else
    return fdopen(fd, mode);
#endif
}
