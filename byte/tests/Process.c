#include <windows.h>
#include <Psapi.h>

#include <stdint.h>
#include <stddef.h>
#include <stdio.h>


typedef struct {
    HANDLE hProcess;
} Process;


void error(const char* message) {
    fprintf(stderr, "error: %s\n", message);
    exit(EXIT_FAILURE);
}

Process Process_new(int pid) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hProcess)
        error("failed to open process");
    
    return (Process){hProcess};
}

Process Process_current(void) {
    HANDLE hProcess = GetCurrentProcess();
    if (!hProcess)
        error("failed to open process");
    
    return (Process){hProcess};
}

void Process_close(const Process* proc) {
    CloseHandle(proc->hProcess);
}

#define Process_write(T) void Process_write_##T(const Process* proc, uintptr_t address, T value) {\
    SIZE_T bytesWritten;\
    if (!WriteProcessMemory(proc->hProcess, (LPVOID)address, &value, sizeof(T), &bytesWritten))\
        error("failed to write to process memory");\
}

#define Process_read(T) T Process_read_##T(const Process* proc, uintptr_t address){\
    SIZE_T bytesRead;\
    T value;\
    if (!ReadProcessMemory(proc->hProcess, (LPCVOID)address, &value, sizeof(T), &bytesRead))\
        error("failed to read process memory");\
    return value;\
}


Process_write(int)
Process_read(int)


void cheat_engine_test(void) {
    // TODO: update with base address and offsets, and also update this when this program is in use
    Process proc = Process_new(20456);
    uintptr_t healthAddress = 0x01465E78;
    Process_write_int(&proc, healthAddress, 1000);
    Process_close(&proc);
}

int main(void) {
    int x = 50;
    printf("x = %d\n", x);
    
    Process proc = Process_current();
    Process_write_int(&proc, (uintptr_t)&x, 100);
    
    printf("x = %d\n", x);
    
    Process_close(&proc);
    return 0;
}
