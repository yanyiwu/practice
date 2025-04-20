#pragma once

#include <string>
#include <vector>
#include "transformer.hpp"

namespace benchmark {

// Base class for all benchmarks
class BenchmarkBase {
public:
    virtual ~BenchmarkBase() = default;
    virtual void run(Transformer& model) = 0;
    virtual std::string name() const = 0;
    virtual float get_accuracy() const = 0;
protected:
    float accuracy = 0.0f;
};

// IWSLT14 German-English Translation benchmark
class IWSLT14Benchmark : public BenchmarkBase {
public:
    IWSLT14Benchmark();
    void run(Transformer& model) override;
    std::string name() const override { return "IWSLT14 De-En"; }
    float get_accuracy() const override { return accuracy; }
private:
    void load_dataset();
    std::vector<std::pair<Matrix, Matrix>> test_pairs;
};

// WMT14 English-German Translation benchmark
class WMT14Benchmark : public BenchmarkBase {
public:
    WMT14Benchmark();
    void run(Transformer& model) override;
    std::string name() const override { return "WMT14 En-De"; }
    float get_accuracy() const override { return accuracy; }
private:
    void load_dataset();
    std::vector<std::pair<Matrix, Matrix>> test_pairs;
};

// GLUE benchmark tasks
class GLUEBenchmark : public BenchmarkBase {
public:
    GLUEBenchmark();
    void run(Transformer& model) override;
    std::string name() const override { return "GLUE"; }
    float get_accuracy() const override { return accuracy; }
private:
    void load_dataset();
    std::vector<std::pair<Matrix, Matrix>> test_pairs;
};

} // namespace benchmark 