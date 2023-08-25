#include <iostream>
#include <cstdint>
#include <cstdio>

#define ELF_NIDENT	16

// program header-ы такого типа нужно загрузить в
// память при загрузке приложения
#define PT_LOAD		1

// структура заголовка ELF файла
struct elf_hdr {
	std::uint8_t e_ident[ELF_NIDENT];
	std::uint16_t e_type;
	std::uint16_t e_machine;
	std::uint32_t e_version;
	std::uint64_t e_entry;
	std::uint64_t e_phoff;
	std::uint64_t e_shoff;
	std::uint32_t e_flags;
	std::uint16_t e_ehsize;
	std::uint16_t e_phentsize;
	std::uint16_t e_phnum;
	std::uint16_t e_shentsize;
	std::uint16_t e_shnum;
	std::uint16_t e_shstrndx;
} __attribute__((packed));

// структура записи в таблице program header-ов
struct elf_phdr {
	std::uint32_t p_type;
	std::uint32_t p_flags;
	std::uint64_t p_offset;
	std::uint64_t p_vaddr;
	std::uint64_t p_paddr;
	std::uint64_t p_filesz;
	std::uint64_t p_memsz;
	std::uint64_t p_align;
} __attribute__((packed));



std::size_t space(const char *name)
{
    // Ваш код здесь, name - имя ELF файла, с которым вы работаете
    // вернуть нужно количество байт, необходимых, чтобы загрузить
    // приложение в память


    struct elf_hdr header;
    std::uint64_t byte_n = 0;

    FILE* file = fopen(name, "rb");

    if (file == NULL) {
        std::cerr << "Unable to open ELF file: " << name << std::endl;
        exit(1);
    }

    if (fread(&header, sizeof(struct elf_hdr), 1, file) != 1) {
        std::cerr << "Unable to read ELF header!" << std::endl;
        exit(1);
    }

    if (fseek(file, header.e_phoff, SEEK_SET) != 0) {
        std::cerr << "Unable to find out program headers!" << std::endl;
        exit(1);
    }

    for (std::uint16_t e_phnum = 0; e_phnum < header.e_phnum; ++e_phnum) {

        struct elf_phdr p_header;

        if (fread(&p_header, sizeof(struct elf_phdr), 1, file) != 1) {
            std::cerr << "Unable to read ELF program header!" << std::endl;
            exit(1);
        }

        if (p_header.p_type == PT_LOAD)
            byte_n += p_header.p_memsz;

    }

    if (fclose(file) != 0) {
		std::cerr << "Unable to close ELF file!" << std::endl;
		exit(1);
	}

    return (std::size_t) byte_n;
}