#include "utils.hpp"
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <iostream>

namespace benchmark {
namespace utils {

bool extract_targz(const std::string& filename, const std::string& target_dir) {
    std::string cmd = "tar -xzf " + filename + " -C " + target_dir;
    return std::system(cmd.c_str()) == 0;
}

std::vector<std::string> read_lines(const std::string& filename) {
    std::vector<std::string> lines;
    std::ifstream file(filename);
    std::string line;
    
    while (std::getline(file, line)) {
        if (!line.empty()) {
            lines.push_back(line);
        }
    }
    
    return lines;
}

std::vector<float> tokenize(const std::string& text, size_t max_length) {
    // This is a very simple tokenization for demonstration
    // In practice, you would use a proper tokenizer
    std::vector<float> tokens;
    std::istringstream iss(text);
    std::string word;
    
    while (iss >> word && tokens.size() < max_length) {
        // Just use the ASCII value of first char as a simple token
        tokens.push_back(static_cast<float>(word[0]));
    }
    
    // Pad to max_length
    while (tokens.size() < max_length) {
        tokens.push_back(0.0f);
    }
    
    return tokens;
}

} // namespace utils
} // namespace benchmark 