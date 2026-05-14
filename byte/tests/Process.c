#include <windows.h>
#include <Psapi.h>

#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>


typedef struct {
    HANDLE hProcess;
} Process;


Process Process_new(int pid) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    assert(hProcess != NULL);
    return (Process){hProcess};
}

Process Process_current(void) {
    HANDLE hProcess = GetCurrentProcess();
    assert(hProcess != NULL);
    return (Process){hProcess};
}

void Process_close(const Process* proc) {
    CloseHandle(proc->hProcess);
}

#define Process_write(T) void Process_write_##T(const Process* proc, uintptr_t address, T value) {\
    SIZE_T bytesWritten;\
    assert(WriteProcessMemory(proc->hProcess, (LPVOID)address, &value, sizeof(T), &bytesWritten));\
}

#define Process_read(T) T Process_read_##T(const Process* proc, uintptr_t address){\
    SIZE_T bytesRead;\
    T value;\
    assert(ReadProcessMemory(proc->hProcess, (LPCVOID)address, &value, sizeof(T), &bytesRead));\
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
    Process proc = Process_current();
    Process_write_int(&proc, (uintptr_t)&x, 100);

    assert(x == 100);
    
    Process_close(&proc);
    return 0;
}
