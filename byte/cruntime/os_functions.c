#include <stdio.h>

#if WINDOWS_TARGET
#include <windows.h>
#endif


FILE* openfd(int fd, const char* mode) {
#if WINDOWS_TARGET
    return __acrt_iob_func(fd);
#else
    return fdopen(fd, mode);
#endif
}

#if WINDOWS_TARGET
int getpid(void) {
    return GetCurrentProcessId();
}
#endif

void sleep(int milliseconds) {
#if WINDOWS_TARGET
    Sleep(milliseconds);
#else
    usleep(milliseconds * 1000);
#endif
}
