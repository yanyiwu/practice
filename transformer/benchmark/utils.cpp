#include "utils.hpp"
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <curl/curl.h>
#include <zlib.h>
#include <archive.h>
#include <archive_entry.h>

namespace {

// CURL write callback
size_t write_data(void* ptr, size_t size, size_t nmemb, FILE* stream) {
    return fwrite(ptr, size, nmemb, stream);
}

// CURL progress callback
int progress_callback(void* clientp, curl_off_t dltotal, curl_off_t dlnow, curl_off_t ultotal, curl_off_t ulnow) {
    if (dltotal == 0) return 0;  // Avoid division by zero
    
    auto* progress_cb = static_cast<benchmark::utils::ProgressCallback*>(clientp);
    if (progress_cb) {
        float progress = static_cast<float>(dlnow) / static_cast<float>(dltotal);
        (*progress_cb)(progress, "Downloading...");
    }
    
    return 0;
}

} // anonymous namespace

namespace benchmark {
namespace utils {

void print_progress(float progress, const std::string& prefix) {
    const int bar_width = 50;
    std::cout << "\r" << prefix << " [";
    int pos = static_cast<int>(bar_width * progress);
    
    for (int i = 0; i < bar_width; ++i) {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    
    std::cout << "] " << std::fixed << std::setprecision(1) << (progress * 100.0) << "%";
    if (progress >= 1.0) std::cout << std::endl;
    std::cout.flush();
}

bool download_file(const std::string& url, const std::string& output_path,
                  const ProgressCallback& progress_cb) {
    CURL* curl = curl_easy_init();
    if (!curl) return false;

    FILE* fp = fopen(output_path.c_str(), "wb");
    if (!fp) {
        curl_easy_cleanup(curl);
        return false;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    
    if (progress_cb) {
        curl_easy_setopt(curl, CURLOPT_XFERINFOFUNCTION, progress_callback);
        curl_easy_setopt(curl, CURLOPT_XFERINFODATA, &progress_cb);
        curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 0L);
    }

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
    fclose(fp);

    return res == CURLE_OK;
}

bool extract_targz(const std::string& filename, const std::string& target_dir,
                  const ProgressCallback& progress_cb) {
    struct archive* a = archive_read_new();
    struct archive* ext = archive_write_disk_new();
    int flags = ARCHIVE_EXTRACT_TIME | ARCHIVE_EXTRACT_PERM | ARCHIVE_EXTRACT_ACL | ARCHIVE_EXTRACT_FFLAGS;
    
    archive_read_support_format_all(a);
    archive_read_support_filter_all(a);
    archive_write_disk_set_options(ext, flags);
    archive_write_disk_set_standard_lookup(ext);
    
    int r = archive_read_open_filename(a, filename.c_str(), 10240);
    if (r != ARCHIVE_OK) {
        std::cerr << "Error opening archive: " << archive_error_string(a) << std::endl;
        return false;
    }
    
    std::filesystem::create_directories(target_dir);
    std::filesystem::current_path(target_dir);
    
    struct archive_entry* entry;
    size_t total_entries = 0;
    size_t processed_entries = 0;
    
    // First count total entries
    while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
        total_entries++;
        archive_read_data_skip(a);
    }
    
    // Reset archive
    archive_read_close(a);
    archive_read_free(a);
    a = archive_read_new();
    archive_read_support_format_all(a);
    archive_read_support_filter_all(a);
    archive_read_open_filename(a, filename.c_str(), 10240);
    
    // Extract files
    while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
        r = archive_write_header(ext, entry);
        if (r != ARCHIVE_OK) {
            std::cerr << "Error writing header: " << archive_error_string(ext) << std::endl;
            continue;
        }
        
        if (archive_entry_size(entry) > 0) {
            const void* buff;
            size_t size;
            la_int64_t offset;
            
            while (archive_read_data_block(a, &buff, &size, &offset) == ARCHIVE_OK) {
                archive_write_data_block(ext, buff, size, offset);
            }
        }
        
        r = archive_write_finish_entry(ext);
        if (r != ARCHIVE_OK) {
            std::cerr << "Error finishing entry: " << archive_error_string(ext) << std::endl;
        }
        
        processed_entries++;
        if (progress_cb) {
            float progress = static_cast<float>(processed_entries) / static_cast<float>(total_entries);
            progress_cb(progress, "Extracting...");
        }
    }
    
    archive_read_close(a);
    archive_read_free(a);
    archive_write_close(ext);
    archive_write_free(ext);
    
    return true;
}

bool extract_zip(const std::string& filename, const std::string& target_dir,
                const ProgressCallback& progress_cb) {
    struct archive* a = archive_read_new();
    struct archive* ext = archive_write_disk_new();
    int flags = ARCHIVE_EXTRACT_TIME | ARCHIVE_EXTRACT_PERM | ARCHIVE_EXTRACT_ACL | ARCHIVE_EXTRACT_FFLAGS;
    
    archive_read_support_format_zip(a);
    archive_write_disk_set_options(ext, flags);
    archive_write_disk_set_standard_lookup(ext);
    
    int r = archive_read_open_filename(a, filename.c_str(), 10240);
    if (r != ARCHIVE_OK) {
        std::cerr << "Error opening zip file: " << archive_error_string(a) << std::endl;
        return false;
    }
    
    std::filesystem::create_directories(target_dir);
    std::filesystem::current_path(target_dir);
    
    struct archive_entry* entry;
    size_t total_entries = 0;
    size_t processed_entries = 0;
    
    // First count total entries
    while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
        total_entries++;
        archive_read_data_skip(a);
    }
    
    // Reset archive
    archive_read_close(a);
    archive_read_free(a);
    a = archive_read_new();
    archive_read_support_format_zip(a);
    archive_read_open_filename(a, filename.c_str(), 10240);
    
    // Extract files
    while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
        r = archive_write_header(ext, entry);
        if (r != ARCHIVE_OK) {
            std::cerr << "Error writing header: " << archive_error_string(ext) << std::endl;
            continue;
        }
        
        if (archive_entry_size(entry) > 0) {
            const void* buff;
            size_t size;
            la_int64_t offset;
            
            while (archive_read_data_block(a, &buff, &size, &offset) == ARCHIVE_OK) {
                archive_write_data_block(ext, buff, size, offset);
            }
        }
        
        r = archive_write_finish_entry(ext);
        if (r != ARCHIVE_OK) {
            std::cerr << "Error finishing entry: " << archive_error_string(ext) << std::endl;
        }
        
        processed_entries++;
        if (progress_cb) {
            float progress = static_cast<float>(processed_entries) / static_cast<float>(total_entries);
            progress_cb(progress, "Extracting...");
        }
    }
    
    archive_read_close(a);
    archive_read_free(a);
    archive_write_close(ext);
    archive_write_free(ext);
    
    return true;
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