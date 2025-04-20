#include "benchmark.hpp"
#include <iostream>
#include <memory>
#include <vector>
#include <iomanip>

int main() {
    // Create transformer model for testing
    Transformer model(512, 6, 8, 2048);  // d_model=512, num_layers=6, num_heads=8, d_ff=2048
    
    // Create benchmarks
    std::vector<std::unique_ptr<benchmark::BenchmarkBase>> benchmarks;
    benchmarks.push_back(std::make_unique<benchmark::IWSLT14Benchmark>());
    benchmarks.push_back(std::make_unique<benchmark::WMT14Benchmark>());
    benchmarks.push_back(std::make_unique<benchmark::GLUEBenchmark>());
    
    // Run benchmarks
    std::cout << "\nRunning Transformer Benchmarks\n";
    std::cout << "============================\n\n";
    
    for (const auto& benchmark : benchmarks) {
        std::cout << "Running " << benchmark->name() << "..." << std::endl;
        benchmark->run(model);
        std::cout << "Accuracy: " << std::fixed << std::setprecision(4) 
                  << benchmark->get_accuracy() * 100 << "%\n" << std::endl;
    }
    
    return 0;
} 