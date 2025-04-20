#include "benchmark.hpp"
#include "utils.hpp"
#include <fstream>
#include <iostream>
#include <cmath>
#include <algorithm>
#include <filesystem>
#include <curl/curl.h>

namespace {

// Helper function to download dataset
size_t write_data(void* ptr, size_t size, size_t nmemb, FILE* stream) {
    return fwrite(ptr, size, nmemb, stream);
}

bool download_file(const std::string& url, const std::string& output_path) {
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

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
    fclose(fp);

    return res == CURLE_OK;
}

// Helper function to compute BLEU score
float compute_bleu_score(const std::vector<float>& output, const std::vector<float>& target) {
    // Simplified BLEU score computation for demonstration
    float match_count = 0;
    for (size_t i = 0; i < output.size() && i < target.size(); ++i) {
        if (std::abs(output[i] - target[i]) < 0.1f) {
            match_count += 1;
        }
    }
    return match_count / std::max(output.size(), target.size());
}

} // anonymous namespace

namespace benchmark {

// IWSLT14 Implementation
IWSLT14Benchmark::IWSLT14Benchmark() {
    load_dataset();
}

void IWSLT14Benchmark::load_dataset() {
    const std::string dataset_url = "https://wit3.fbk.eu/archive/2014-01/texts/de/en/de-en.tgz";
    const std::string dataset_path = "benchmark/data/iwslt14/";
    const std::string targz_file = dataset_path + "de-en.tgz";
    
    std::filesystem::create_directories(dataset_path);
    
    if (!std::filesystem::exists(targz_file)) {
        std::cout << "Downloading IWSLT14 dataset..." << std::endl;
        if (!download_file(dataset_url, targz_file)) {
            std::cerr << "Failed to download IWSLT14 dataset" << std::endl;
            return;
        }
        
        std::cout << "Extracting IWSLT14 dataset..." << std::endl;
        if (!utils::extract_targz(targz_file, dataset_path)) {
            std::cerr << "Failed to extract IWSLT14 dataset" << std::endl;
            return;
        }
    }

    // Load test data
    const std::string test_de = dataset_path + "test.de";
    const std::string test_en = dataset_path + "test.en";
    
    if (!std::filesystem::exists(test_de) || !std::filesystem::exists(test_en)) {
        std::cerr << "Test files not found" << std::endl;
        return;
    }
    
    auto de_lines = utils::read_lines(test_de);
    auto en_lines = utils::read_lines(test_en);
    
    size_t num_samples = std::min(de_lines.size(), en_lines.size());
    for (size_t i = 0; i < num_samples; ++i) {
        Matrix input = {utils::tokenize(de_lines[i])};
        Matrix target = {utils::tokenize(en_lines[i])};
        test_pairs.push_back(std::make_pair(input, target));
    }
    
    std::cout << "Loaded " << test_pairs.size() << " test pairs" << std::endl;
}

void IWSLT14Benchmark::run(Transformer& model) {
    float total_bleu = 0.0f;
    
    for (const auto& pair : test_pairs) {
        auto output = model.forward(pair.first);
        
        // Compute BLEU score for this sample
        float bleu = 0.0f;
        for (size_t i = 0; i < output.size(); ++i) {
            bleu += compute_bleu_score(output[i], pair.second[i]);
        }
        bleu /= output.size();
        total_bleu += bleu;
    }
    
    accuracy = total_bleu / test_pairs.size();
}

// WMT14 Implementation
WMT14Benchmark::WMT14Benchmark() {
    load_dataset();
}

void WMT14Benchmark::load_dataset() {
    const std::string dataset_url = "http://www.statmt.org/wmt14/training-parallel-nc-v9.tgz";
    const std::string dataset_path = "benchmark/data/wmt14/";
    const std::string targz_file = dataset_path + "training-parallel-nc-v9.tgz";
    
    std::filesystem::create_directories(dataset_path);
    
    if (!std::filesystem::exists(targz_file)) {
        std::cout << "Downloading WMT14 dataset..." << std::endl;
        if (!download_file(dataset_url, targz_file)) {
            std::cerr << "Failed to download WMT14 dataset" << std::endl;
            return;
        }
        
        std::cout << "Extracting WMT14 dataset..." << std::endl;
        if (!utils::extract_targz(targz_file, dataset_path)) {
            std::cerr << "Failed to extract WMT14 dataset" << std::endl;
            return;
        }
    }

    // Load test data
    const std::string test_en = dataset_path + "test.en";
    const std::string test_de = dataset_path + "test.de";
    
    if (!std::filesystem::exists(test_en) || !std::filesystem::exists(test_de)) {
        std::cerr << "Test files not found" << std::endl;
        return;
    }
    
    auto en_lines = utils::read_lines(test_en);
    auto de_lines = utils::read_lines(test_de);
    
    size_t num_samples = std::min(en_lines.size(), de_lines.size());
    for (size_t i = 0; i < num_samples; ++i) {
        Matrix input = {utils::tokenize(en_lines[i])};
        Matrix target = {utils::tokenize(de_lines[i])};
        test_pairs.push_back(std::make_pair(input, target));
    }
    
    std::cout << "Loaded " << test_pairs.size() << " test pairs" << std::endl;
}

void WMT14Benchmark::run(Transformer& model) {
    float total_bleu = 0.0f;
    
    for (const auto& pair : test_pairs) {
        auto output = model.forward(pair.first);
        
        // Compute BLEU score for this sample
        float bleu = 0.0f;
        for (size_t i = 0; i < output.size(); ++i) {
            bleu += compute_bleu_score(output[i], pair.second[i]);
        }
        bleu /= output.size();
        total_bleu += bleu;
    }
    
    accuracy = total_bleu / test_pairs.size();
}

// GLUE Implementation
GLUEBenchmark::GLUEBenchmark() {
    load_dataset();
}

void GLUEBenchmark::load_dataset() {
    const std::string dataset_path = "benchmark/data/glue/";
    std::filesystem::create_directories(dataset_path);
    
    // GLUE consists of multiple tasks, we'll focus on a few key ones:
    const std::vector<std::pair<std::string, std::string>> tasks = {
        {"CoLA", "https://dl.fbaipublicfiles.com/glue/data/CoLA.zip"},
        {"SST-2", "https://dl.fbaipublicfiles.com/glue/data/SST-2.zip"},
        {"MRPC", "https://dl.fbaipublicfiles.com/glue/data/MRPC.zip"},
        {"QQP", "https://dl.fbaipublicfiles.com/glue/data/QQP.zip"}
    };
    
    for (const auto& [task, url] : tasks) {
        const std::string task_path = dataset_path + task;
        const std::string zip_file = task_path + ".zip";
        
        if (!std::filesystem::exists(zip_file)) {
            std::cout << "Downloading GLUE " << task << " dataset..." << std::endl;
            if (!download_file(url, zip_file)) {
                std::cerr << "Failed to download " << task << std::endl;
                continue;
            }
            
            // TODO: Extract zip file
        }
        
        // Load test data
        const std::string test_file = task_path + "/test.tsv";
        if (!std::filesystem::exists(test_file)) {
            std::cerr << "Test file not found for " << task << std::endl;
            continue;
        }
        
        auto lines = utils::read_lines(test_file);
        for (const auto& line : lines) {
            Matrix input = {utils::tokenize(line)};
            Matrix target = {utils::tokenize(line)};  // For demonstration, use same line as target
            test_pairs.push_back(std::make_pair(input, target));
        }
    }
    
    std::cout << "Loaded " << test_pairs.size() << " GLUE test samples" << std::endl;
}

void GLUEBenchmark::run(Transformer& model) {
    float total_accuracy = 0.0f;
    
    for (const auto& pair : test_pairs) {
        auto output = model.forward(pair.first);
        
        // For GLUE tasks, we typically use accuracy or F1 score
        float task_score = 0.0f;
        for (size_t i = 0; i < output.size(); ++i) {
            // Simplified accuracy computation
            float match = compute_bleu_score(output[i], pair.second[i]);
            task_score += match;
        }
        task_score /= output.size();
        total_accuracy += task_score;
    }
    
    accuracy = total_accuracy / test_pairs.size();
}

} // namespace benchmark 