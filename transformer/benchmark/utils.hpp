#pragma once

#include <string>
#include <vector>
#include <filesystem>

namespace benchmark {
namespace utils {

// Extract tar.gz file
bool extract_targz(const std::string& filename, const std::string& target_dir);

// Load text file and split into lines
std::vector<std::string> read_lines(const std::string& filename);

// Simple tokenization
std::vector<float> tokenize(const std::string& text, size_t max_length = 512);

} // namespace utils
} // namespace benchmark 