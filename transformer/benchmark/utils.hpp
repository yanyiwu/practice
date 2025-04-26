#pragma once

#include <string>
#include <vector>
#include <filesystem>
#include <functional>

namespace benchmark {
namespace utils {

// Progress callback type
using ProgressCallback = std::function<void(float progress, const std::string& message)>;

// Extract tar.gz file
bool extract_targz(const std::string& filename, const std::string& target_dir, 
                  const ProgressCallback& progress_cb = nullptr);

// Extract zip file
bool extract_zip(const std::string& filename, const std::string& target_dir,
                const ProgressCallback& progress_cb = nullptr);

// Load text file and split into lines
std::vector<std::string> read_lines(const std::string& filename);

// Simple tokenization
std::vector<float> tokenize(const std::string& text, size_t max_length = 512);

// Download file with progress reporting
bool download_file(const std::string& url, const std::string& output_path,
                  const ProgressCallback& progress_cb = nullptr);

// Print progress bar
void print_progress(float progress, const std::string& prefix = "");

} // namespace utils
} // namespace benchmark 