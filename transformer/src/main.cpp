#include "transformer.hpp"
#include <iostream>
#include <random>
#include <iomanip>
#include <cmath>
#include <numeric>

// 生成随机序列
Matrix generate_random_sequence(int seq_len, int d_model) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<float> dist(0.0f, 0.01f);
    
    Matrix sequence(seq_len, std::vector<float>(d_model));
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_model; ++j) {
            sequence[i][j] = dist(gen);
        }
    }
    return sequence;
}

// 计算均方误差
float compute_mse(const Matrix& output, const Matrix& target) {
    float mse = 0.0f;
    int seq_len = output.size();
    int d_model = output[0].size();
    
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_model; ++j) {
            float diff = output[i][j] - target[i][j];
            mse += diff * diff;
        }
    }
    
    return mse / (seq_len * d_model);
}

// 计算相对误差
float compute_relative_error(const Matrix& output, const Matrix& target) {
    float rel_error = 0.0f;
    float target_norm = 0.0f;
    int seq_len = output.size();
    int d_model = output[0].size();
    
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_model; ++j) {
            float diff = std::abs(output[i][j] - target[i][j]);
            rel_error += diff;
            target_norm += std::abs(target[i][j]);
        }
    }
    
    return rel_error / (target_norm + 1e-6f);
}

// 打印序列的前几个位置和特征
void print_sequence(const Matrix& sequence, const std::string& name) {
    std::cout << name << " (showing first 3 positions, first 3 features):" << std::endl;
    for (int i = 0; i < std::min(3, static_cast<int>(sequence.size())); ++i) {
        std::cout << "Position " << i << ": ";
        for (int j = 0; j < std::min(3, static_cast<int>(sequence[i].size())); ++j) {
            std::cout << std::fixed << std::setprecision(4) << sequence[i][j] << " ";
        }
        std::cout << "..." << std::endl;
    }
    std::cout << std::endl;
}

// 裁剪梯度
void clip_gradients(Matrix& gradients, float max_norm) {
    float norm = 0.0f;
    
    // 计算梯度范数
    for (const auto& row : gradients) {
        for (float g : row) {
            if (std::isnan(g)) {
                std::cout << "Warning: NaN gradient detected!" << std::endl;
                return;
            }
            norm += g * g;
        }
    }
    norm = std::sqrt(norm);
    
    // 如果范数超过阈值，则缩放梯度
    if (norm > max_norm) {
        float scale = max_norm / (norm + 1e-6f);
        for (auto& row : gradients) {
            for (float& g : row) {
                g *= scale;
            }
        }
    }
}

// 计算余弦学习率调度
float get_learning_rate(float initial_lr, int epoch, int warmup_steps, int total_steps) {
    float progress = static_cast<float>(epoch) / total_steps;
    if (epoch < warmup_steps) {
        return initial_lr * static_cast<float>(epoch) / warmup_steps;
    }
    return initial_lr * (1.0f + std::cos(M_PI * progress)) / 2.0f;
}

int main() {
    // Transformer parameters
    const int d_model = 16;     // 减小模型维度
    const int num_heads = 2;    // 减少注意力头数
    const int num_layers = 1;   // 减少层数
    const int d_ff = 32;        // 减小前馈网络维度
    const int seq_len = 8;      // 保持序列长度不变
    
    // Training parameters
    const int num_epochs = 2000;          // 增加训练轮数
    const float initial_lr = 0.0001f;     // 增加初始学习率
    const int print_every = 100;
    const float max_grad_norm = 0.1f;     // 进一步减小梯度裁剪阈值
    const int warmup_steps = 200;         // 增加预热步数
    const float min_improvement = 0.0001f; // 最小改进阈值
    
    // Create transformer
    Transformer transformer(d_model, num_layers, num_heads, d_ff);
    
    // Training loop
    std::cout << "Starting training...\n" << std::endl;
    std::cout << "Model configuration:" << std::endl;
    std::cout << "d_model: " << d_model << std::endl;
    std::cout << "num_heads: " << num_heads << std::endl;
    std::cout << "num_layers: " << num_layers << std::endl;
    std::cout << "d_ff: " << d_ff << std::endl;
    std::cout << "seq_len: " << seq_len << std::endl;
    std::cout << "\n------------------------\n" << std::endl;
    
    float best_loss = std::numeric_limits<float>::infinity();
    int no_improvement_count = 0;
    std::vector<float> loss_history;
    
    for (int epoch = 0; epoch < num_epochs; ++epoch) {
        // Calculate current learning rate
        float current_lr = get_learning_rate(initial_lr, epoch, warmup_steps, num_epochs);
        
        // Generate random input sequence
        auto input_sequence = generate_random_sequence(seq_len, d_model);
        auto target_sequence = input_sequence;
        
        // Forward pass
        auto output_sequence = transformer.forward(input_sequence);
        
        // Check for NaN in output
        bool has_nan = false;
        for (const auto& row : output_sequence) {
            for (float val : row) {
                if (std::isnan(val)) {
                    has_nan = true;
                    break;
                }
            }
            if (has_nan) break;
        }
        
        if (has_nan) {
            std::cout << "Training failed: NaN detected in model output at epoch " << (epoch + 1) << std::endl;
            break;
        }
        
        // Compute metrics
        float loss = compute_mse(output_sequence, target_sequence);
        float rel_error = compute_relative_error(output_sequence, target_sequence);
        loss_history.push_back(loss);
        
        // Early stopping check with minimum improvement threshold
        if (loss < best_loss - min_improvement) {
            best_loss = loss;
            no_improvement_count = 0;
        } else {
            no_improvement_count++;
            if (no_improvement_count > 200) {  // 增加早停的容忍度
                std::cout << "Early stopping at epoch " << (epoch + 1) << std::endl;
                break;
            }
        }
        
        // Backward pass
        auto loss_gradient = transformer.compute_loss_gradient(output_sequence, target_sequence);
        clip_gradients(loss_gradient, max_grad_norm);
        transformer.backward(loss_gradient);
        transformer.update_weights(current_lr);
        
        // Print progress
        if ((epoch + 1) % print_every == 0) {
            // Calculate average loss over last print_every epochs
            float avg_loss = 0.0f;
            for (int i = std::max(0, static_cast<int>(loss_history.size()) - print_every);
                 i < loss_history.size(); ++i) {
                avg_loss += loss_history[i];
            }
            avg_loss /= std::min(print_every, static_cast<int>(loss_history.size()));
            
            std::cout << "Epoch " << (epoch + 1) 
                      << ", Loss: " << loss 
                      << ", Avg Loss: " << avg_loss
                      << ", Rel Error: " << rel_error
                      << ", LR: " << current_lr << std::endl;
            
            if (epoch == 0 || (epoch + 1) % (print_every * 5) == 0) {
                std::cout << "\nSample comparison:" << std::endl;
                print_sequence(input_sequence, "Input");
                print_sequence(output_sequence, "Output");
                print_sequence(target_sequence, "Target");
                std::cout << "------------------------\n" << std::endl;
            }
        }
    }
    
    std::cout << "Training completed!" << std::endl;
    std::cout << "Best loss achieved: " << best_loss << std::endl;
    
    // Final evaluation
    auto test_input = generate_random_sequence(seq_len, d_model);
    auto test_output = transformer.forward(test_input);
    float final_loss = compute_mse(test_output, test_input);
    float final_rel_error = compute_relative_error(test_output, test_input);
    
    std::cout << "\nFinal evaluation:" << std::endl;
    std::cout << "Test MSE: " << final_loss << std::endl;
    std::cout << "Test Relative Error: " << final_rel_error << std::endl;
    
    return 0;
} 