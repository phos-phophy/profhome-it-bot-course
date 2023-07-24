#include <cstdio>


struct ALLOCATOR {
    void* start;
    std::size_t size;
} my_allocator;

struct HEADER {
    bool free;
    std::size_t size;
};

struct TAIL {
    bool free;
    std::size_t size;
};

bool is_first_block(const struct HEADER* header){
    return header == (struct HEADER*)my_allocator.start;
}

bool is_last_block(const struct TAIL* tail){
    return tail == (struct TAIL*)((unsigned char*)my_allocator.start + my_allocator.size - sizeof(struct TAIL));
}

// Эта функция будет вызвана перед тем как вызывать myalloc и myfree
// используйте ее чтобы инициализировать ваш аллокатор перед началом
// работы.
//
// buf - указатель на участок логической памяти, который ваш аллокатор
//       должен распределять, все возвращаемые указатели должны быть
//       либо равны NULL, либо быть из этого участка памяти
// size - размер участка памяти, на который указывает buf
void mysetup(void *buf, std::size_t size) {
    my_allocator.start = buf;
    my_allocator.size = size;

    struct HEADER* header = (struct HEADER*)buf;
    header->free = true;
    header->size = size - sizeof(struct HEADER) - sizeof(struct TAIL);

    struct TAIL* tail = (struct TAIL*)((unsigned char*)buf + size - sizeof(struct TAIL));
    tail->free = true;
    tail->size = size - sizeof(struct HEADER) - sizeof(struct TAIL);
}

// Функция аллокации
void *myalloc(std::size_t size) {
    struct HEADER* candidate_block = (struct HEADER*)my_allocator.start;

    // search for a suitable block
    while (candidate_block->free == false || candidate_block->size < size) {
        struct TAIL* block_tail = (struct TAIL*)((unsigned char*)candidate_block + sizeof(struct HEADER) + candidate_block->size);

        if (is_last_block(block_tail))
            break;

        candidate_block = (struct HEADER*)(block_tail + 1);
    }

    if (candidate_block->free == false || candidate_block->size < size)
        return NULL;

    std::size_t remaining_size = candidate_block->size - size;
    struct TAIL* block_tail = (struct TAIL*)((unsigned char*)candidate_block + sizeof(struct HEADER) + candidate_block->size);

    // allocate memory
    if (remaining_size >= sizeof(struct HEADER) + sizeof(struct TAIL)){
        struct HEADER* new_header = (struct HEADER*)((unsigned char*)candidate_block + size + sizeof(struct TAIL) + sizeof(struct HEADER));

        new_header->free = true;
        new_header->size = remaining_size - sizeof(struct HEADER) - sizeof(struct TAIL);
        block_tail->size = remaining_size - sizeof(struct HEADER) - sizeof(struct TAIL);

        block_tail = (struct TAIL*)new_header - 1;
        candidate_block->size = size;
        block_tail->size = size;
    }

    block_tail->free = false;
    candidate_block->free = false;

    return (void *)(candidate_block + 1);
}

// Функция освобождения
void myfree(void *p) {
    struct HEADER* header = (struct HEADER*)p - 1;
    struct TAIL* tail = (struct TAIL*)((unsigned char*)p + header->size);

    header->free = true;
    tail->free = true;

    size_t new_size = header->size;

    // try to combine block with previos one
    if (!is_first_block(header)) {
        struct TAIL* prev_tail = (struct TAIL*)header - 1;
        if (prev_tail->free == true) {
            new_size += prev_tail->size + sizeof(struct HEADER) + sizeof(struct TAIL);
            header = (struct HEADER*)((unsigned char*)prev_tail - prev_tail->size - sizeof(struct HEADER));
        } 
    }

    // try to combine block with next one
    if (!is_last_block(tail)) {
        struct HEADER* next_header = (struct HEADER*)(tail + 1);
        if (next_header->free == true) {
            new_size += next_header->size + sizeof(struct HEADER) + sizeof(struct TAIL);
            tail = (struct TAIL*)((unsigned char*)next_header + sizeof(struct HEADER) + next_header->size);
        }
    }

    header->size = new_size;
    tail->size = new_size;
}