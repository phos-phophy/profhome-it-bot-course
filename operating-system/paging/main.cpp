#include <iostream>
#include <fstream>
#include <string>
#include <map>


struct PAGE {
    uint16_t pml4;
    uint16_t directory_ptr;
    uint16_t directory;
    uint16_t table;
    uint16_t offset;
};


PAGE build_logical_page(const uint64_t& logical_address) {
    struct PAGE logical_page {
        static_cast<uint16_t>((logical_address >> 39) & 0x1ff),
        static_cast<uint16_t>((logical_address >> 30) & 0x1ff), 
        static_cast<uint16_t>((logical_address >> 21) & 0x1ff), 
        static_cast<uint16_t>((logical_address >> 12) & 0x1ff), 
        static_cast<uint16_t>(logical_address & 0xfff)
    };
    return logical_page;
}


uint64_t get_next_value(
    std::ofstream& outfile,
    const std::map<uint64_t, uint64_t>& memory_structure,
    const uint64_t& table,
    const uint64_t& index
){
    auto v = memory_structure.find(table + index);
    if (v != memory_structure.end() && v->second & 1 != 0)
        return v->second & 0xfffffffff000;
    outfile << "fault\n";
    return 0;
}


void convert(
    std::ofstream& outfile, 
    const std::map<uint64_t, uint64_t>& memory_structure,
    const uint64_t& logical_address,
    const uint64_t& root_table
) {
    struct PAGE logical_page = build_logical_page(logical_address);

    uint64_t value = root_table;

    value = get_next_value(outfile, memory_structure, value, logical_page.pml4 * 8u);
    if (value == 0) return;
    value = get_next_value(outfile, memory_structure, value, logical_page.directory_ptr * 8u);
    if (value == 0) return;
    value = get_next_value(outfile, memory_structure, value, logical_page.directory * 8u);
    if (value == 0) return;
    value = get_next_value(outfile, memory_structure, value, logical_page.table * 8u);
    if (value == 0) return;

    outfile << value + logical_page.offset << "\n";
}


int main() {
    std::string dataset;
    std::cout << "Enter dataset name: ";
    std::cin >> dataset;

    std::string output_file;
    std::cout << "Enter output file: ";
    std::cin >> output_file;

    std::ifstream infile(dataset);
    std::ofstream outfile(output_file);

    int m, q;
    uint64_t root_table; 
    infile >> m >> q >> root_table;

    uint64_t paddr, value;
    std::map <uint64_t, uint64_t> memory_structure;
    for(int i = 0; i < m; ++i) {
        infile >> paddr >> value;
        memory_structure.insert({paddr, value});
    }

    uint64_t logical_address;
    for(int i = 0; i < q; ++i){
        infile >> logical_address;
        convert(outfile, memory_structure, logical_address, root_table);
    }

    return 0;
}