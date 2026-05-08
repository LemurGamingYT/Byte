#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>


typedef struct {
    unsigned int bits;
    int size;
} BitField;


// TODO: bitwise operations

BitField BitField_new(int size) {
    return (BitField){0, size};
}

void BitField_set(BitField* bf, int index, bool active) {
    assert(index < bf->size);
    if (active)
        bf->bits |= (1u << index);
    else
        bf->bits &= ~(1u << index);
}

bool BitField_get(const BitField* bf, int index) {
    return (bf->bits >> index) & 1u;
}


int main(void) {
    BitField bf = BitField_new(20);
    BitField_set(&bf, 16, true);
    
    printf("%u\n", bf.bits);
    return 0;
}
