#include <iostream>
#include <cstdint>
#include <cstdio>

#define ELF_NIDENT	16


// Эта структура описывает формат заголовока ELF файла
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


std::uintptr_t entry_point(const char *name)
{
	struct elf_hdr header;
	FILE* file = fopen(name, "rb");

	if (file == NULL) {
        std::cerr << "Unable to open ELF file: " << name << std::endl;
        exit(1);
    }

	if (fread(&header, sizeof(struct elf_hdr), 1, file) != 1) {
		std::cerr << "Unable to read ELF header!" << std::endl;
        exit(1);
	}

	if (fclose(file) != 0) {
		std::cerr << "Unable to close ELF file!" << std::endl;
		exit(1);
	}

	return (std::uintptr_t) header.e_entry;
}