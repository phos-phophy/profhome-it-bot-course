#include <cstdio>
#include <iostream>
#include <algorithm>

#define SLAB_BLOCK_MIN_NUM 16

/**
 * Эти две функции вы должны использовать для аллокации
 * и освобождения памяти в этом задании. Считайте, что
 * внутри они используют buddy аллокатор с размером
 * страницы равным 4096 байтам.
 **/

/**
 * Аллоцирует участок размером 4096 * 2^order байт,
 * выровненный на границу 4096 * 2^order байт. order
 * должен быть в интервале [0; 10] (обе границы
 * включительно), т. е. вы не можете аллоцировать больше
 * 4Mb за раз.
 **/
void *alloc_slab(int order);
/**
 * Освобождает участок ранее аллоцированный с помощью
 * функции alloc_slab.
 **/
void free_slab(void *slab);


struct slab_block;


struct slab_header {
    struct slab_header *next_slab;
    struct slab_header *prev_slab;
    struct slab_block *free_block;
    size_t free_counter;
};


struct slab_block {
    struct slab_block *next_block;
};


/**
 * Эта структура представляет аллокатор, вы можете менять
 * ее как вам удобно. Приведенные в ней поля и комментарии
 * просто дают общую идею того, что вам может понадобится
 * сохранить в этой структуре.
 **/
struct cache {
    struct slab_header *free_slab; /* список пустых SLAB-ов для поддержки cache_shrink */
    struct slab_header *filled_slab; /* список заполненых SLAB-ов */
    struct slab_header *slab; /* список частично занятых SLAB-ов */

    size_t object_size; /* размер аллоцируемого объекта */
    int slab_order; /* используемый размер SLAB-а */
    size_t slab_objects; /* количество объектов в одном SLAB-е */ 
};


/**
 * Функция инициализации будет вызвана перед тем, как
 * использовать этот кеширующий аллокатор для аллокации.
 * Параметры:
 *  - cache - структура, которую вы должны инициализировать
 *  - object_size - размер объектов, которые должен
 *    аллоцировать этот кеширующий аллокатор 
 **/
void cache_setup(struct cache *cache, size_t object_size)
{
    cache->free_slab = NULL;
    cache->filled_slab = NULL;
    cache->slab = NULL;

    cache->object_size = std::max(object_size, sizeof(struct slab_block));

    size_t required_memory = sizeof(struct slab_header) + SLAB_BLOCK_MIN_NUM * cache->object_size;

    int order = 0;
    while ((1UL << order) * 4096 < required_memory) ++order;
    cache->slab_order = order;

    cache->slab_objects = ((1UL << order) * 4096 - sizeof(struct slab_header)) / cache->object_size;
}


void slab_chain_release(struct slab_header **slab_ptr);


/**
 * Функция освобождения будет вызвана когда работа с
 * аллокатором будет закончена. Она должна освободить
 * всю память занятую аллокатором. Проверяющая система
 * будет считать ошибкой, если не вся память будет
 * освбождена.
 **/
void cache_release(struct cache *cache)
{
    slab_chain_release(&cache->filled_slab);
    slab_chain_release(&cache->free_slab);
    slab_chain_release(&cache->slab);
}


void move_slab(struct slab_header **from, struct slab_header **to, bool backward_ref)
{
    if (*from == NULL) return; 

    struct slab_header *slab = *from;

    if (slab->next_slab != NULL)
        if (backward_ref)
            slab->next_slab->prev_slab = *from;
        else
            slab->next_slab->prev_slab = NULL;

    *from = slab->next_slab;

    slab->next_slab = *to;
    *to = slab;

    if (slab->next_slab != NULL)
        slab->next_slab->prev_slab = slab;
}


/**
 * Функция аллокации памяти из кеширующего аллокатора.
 * Должна возвращать указатель на участок памяти размера
 * как минимум object_size байт (см cache_setup).
 * Гарантируется, что cache указывает на корректный
 * инициализированный аллокатор.
 **/
void *cache_alloc(struct cache *cache)
{
    // allocate space from common slab
    if (cache->slab != NULL) {
        struct slab_header* slab = cache->slab;
        struct slab_block* slab_block = slab->free_block;

        slab->free_block = slab_block->next_block;
        slab->free_counter--;

        if (slab->free_block == NULL)
            move_slab(&cache->slab, &cache->filled_slab, false);

        return slab_block;
    } 

    // allocate space from empty slab
    if (cache->free_slab != NULL) {
        struct slab_header* slab = cache->free_slab;
        struct slab_block* slab_block = slab->free_block;

        slab->free_block = slab_block->next_block;
        slab->free_counter--;

        if (slab->free_block == NULL)
            move_slab(&cache->free_slab, &cache->filled_slab, false);
        else
            move_slab(&cache->free_slab, &cache->slab, false);

        return slab_block;
    } 

    // create new slab and try to allocate memory again
    struct slab_header *new_slab = (struct slab_header *)alloc_slab(cache->slab_order);
    new_slab->next_slab = cache->free_slab;
    cache->free_slab = new_slab;
    new_slab->prev_slab = NULL;

    if (new_slab->next_slab != NULL)
        new_slab->next_slab->prev_slab = new_slab;

    new_slab->free_counter = cache->slab_objects;
    new_slab->free_block = (struct slab_block*)((unsigned char*) new_slab + sizeof(struct slab_header));
    new_slab->free_block->next_block = NULL;

    struct slab_block *prev_block = new_slab->free_block;
    for (size_t i = 1; i < cache->slab_objects; i++) {
        prev_block->next_block = (struct slab_block*)((unsigned char*)prev_block + cache->object_size);
        prev_block->next_block->next_block = NULL;
        prev_block = prev_block->next_block;
    }

    return cache_alloc(cache);
}


/**
 * Функция освобождения памяти назад в кеширующий аллокатор.
 * Гарантируется, что ptr - указатель ранее возвращенный из
 * cache_alloc.
 **/
void cache_free(struct cache *cache, void *ptr)
{
    struct slab_header *slab = (struct slab_header *)(((uint64_t) ptr >> (cache->slab_order + 12)) << (cache->slab_order + 12));

    struct slab_block *block = (struct slab_block *)ptr;
    block->next_block = slab->free_block;
    slab->free_block = block;

    ++slab->free_counter;

    if (slab->free_counter != 1 && slab->free_counter != cache->slab_objects)
        return;

    struct slab_header **from;
    struct slab_header **to;

    if (slab->free_counter == cache->slab_objects)
        to = &cache->free_slab;
    else
        to = &cache->slab;

    bool backward_ref = false;

    if (slab->prev_slab != NULL) {
        from = &slab->prev_slab;
        backward_ref = true;
    } else if (slab == cache->slab)
        from = &cache->slab;
    else
        from = &cache->filled_slab;

    move_slab(from, to, backward_ref);
}


/**
 * Функция должна освободить все SLAB, которые не содержат
 * занятых объектов. Если SLAB не использовался для аллокации
 * объектов (например, если вы выделяли с помощью alloc_slab
 * память для внутренних нужд вашего алгоритма), то освобождать
 * его не обязательно.
 **/
void cache_shrink(struct cache *cache)
{
    slab_chain_release(&cache->free_slab);
}


void slab_chain_release(struct slab_header **slab_ptr) {
    struct slab_header *slab = *slab_ptr;

    while (slab != NULL) {
        struct slab_header *next_slab = slab->next_slab;

        struct slab_block *free_block = slab->free_block;

        while (free_block != NULL) {
            struct slab_block *next_free_block = free_block->next_block;
            free_block->next_block = NULL;
            free_block = next_free_block;
        }

        slab->next_slab = NULL;
        slab->prev_slab = NULL;
        slab->free_block = NULL;

        free_slab(slab);

        slab = next_slab;
    }

    *slab_ptr = NULL;
}
