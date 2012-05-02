#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <stdint.h>

#ifdef _WIN32
	#include <Windows.h>
#else
	#include <sys/mman.h>
#endif

int main(int argc, char *argv[])
{
        uint8_t *executable = NULL, *new_stack = NULL;
        FILE *fd = NULL;
        uint32_t size = 0, i = 0;
		
        if(argc != 2) {
                printf("Usage: %s <shellcode>\n", argv[0]);
                exit(1);
        } 
        // Open the file
        if((fd = fopen(argv[1], "r")) == NULL) {
                printf("Error opening shellcode file\n");
                exit(1);
        }

        // Get the file size
        fseek(fd, 0, SEEK_END);
        size = ftell(fd);
        fseek(fd, 0, SEEK_SET);

#ifdef _WIN32
        // We need some more memory to work
	if((executable = (uint8_t *)VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)) == NULL) {
                printf("Failed to allocate memory for shellcode\n");
                exit(1);
        }

        // Allocate a new stack
	if((new_stack = (uint8_t *)VirtualAlloc(NULL, 0x200000, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE)) == NULL) {
                printf("Failed to allocate memory for stack\n");
                exit(1);
	}
#else
        // We need some more memory to work
        if((executable = mmap(
                        NULL, size,
                        PROT_EXEC | PROT_READ | PROT_WRITE,
                        MAP_ANONYMOUS | MAP_SHARED,
                        -1, 0)) == MAP_FAILED) {
                printf("Failed to allocate memory\n");
                exit(1);
        }

        // Allocate a new stack
        if ((new_stack = mmap(
                        NULL, 0x200000,
                        PROT_EXEC | PROT_READ | PROT_WRITE,
                        MAP_ANONYMOUS | MAP_SHARED,
                        -1, 0)) == MAP_FAILED) {
                printf("Failed to allocate new stack\n");
                exit(1);
        }
#endif


        // Read the shellcode to memory
	for(i = 0; i < size; i++) {
		executable[i] = fgetc(fd);
	}

        if(i != size) {
		printf("Failed to read entire shellcode file: %d\n", i);
		exit(1);
	}

        // This is no longer needed
        fclose(fd);

	printf("Shellcode size: %d\n", size);
        printf("Shellcode address: 0x%08x\n", executable);
        printf("Stack address: 0x%08x\n", new_stack);

#ifdef _WIN32
        // Set up the stack and jump to our code
	__asm {
		mov eax, [ebp - 8]
		mov esp, [ebp - 12]
		add esp, 0x100000
		int 3
		jmp eax
	}
#else
	// Set up the stack and jump to our code
        __asm__("mov -0x2c(%ebp),%eax");
        __asm__("mov -0x28(%ebp),%esp");
        __asm__("add $0x100000, %esp");
	__asm__("int3");
        __asm__("jmp *%eax");
#endif

}

