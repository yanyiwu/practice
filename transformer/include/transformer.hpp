#pragma once

#include <vector>
#include <random>
#include <cmath>
#include <memory>

using Matrix = std::vector<std::vector<float>>;

class MultiHeadAttention {
public:
    MultiHeadAttention(int d_model, int num_heads);
    Matrix forward(const Matrix& query, const Matrix& key, const Matrix& value);
    Matrix backward(const Matrix& grad_output);
    void update_weights(float learning_rate);

private:
    int d_model;
    int num_heads;
    int d_k;
    
    Matrix W_q;
    Matrix W_k;
    Matrix W_v;
    Matrix W_o;
    
    // 存储前向传播的中间结果，用于反向传播
    Matrix last_query;
    Matrix last_key;
    Matrix last_value;
    Matrix last_attention_scores;
    Matrix last_attention_output;
    
    // 梯度
    Matrix grad_W_q;
    Matrix grad_W_k;
    Matrix grad_W_v;
    Matrix grad_W_o;
    
    void initialize_weights();
    Matrix scaled_dot_product_attention(const Matrix& Q, const Matrix& K, const Matrix& V);
    Matrix scaled_dot_product_attention_backward(const Matrix& grad_output);
};

class FeedForward {
public:
    FeedForward(int d_model, int d_ff);
    Matrix forward(const Matrix& x);
    Matrix backward(const Matrix& grad_output);
    void update_weights(float learning_rate);

private:
    int d_model;
    int d_ff;
    Matrix W1;
    Matrix W2;
    std::vector<float> b1;
    std::vector<float> b2;
    
    // 存储前向传播的中间结果
    Matrix last_input;
    Matrix last_hidden;
    
    // 梯度
    Matrix grad_W1;
    Matrix grad_W2;
    std::vector<float> grad_b1;
    std::vector<float> grad_b2;
    
    void initialize_weights();
};

class TransformerLayer {
public:
    TransformerLayer(int d_model, int num_heads, int d_ff);
    Matrix forward(const Matrix& x);
    Matrix backward(const Matrix& grad_output);
    void update_weights(float learning_rate);

private:
    std::unique_ptr<MultiHeadAttention> self_attention;
    std::unique_ptr<FeedForward> feed_forward;
    
    // 存储前向传播的中间结果
    Matrix last_input;
    Matrix last_attention_output;
    Matrix last_norm1_output;
    Matrix last_ff_output;
    Matrix last_norm2_output;
    
    Matrix layer_norm(const Matrix& x);
    Matrix layer_norm_backward(const Matrix& grad_output, const Matrix& last_input);
};

class Transformer {
public:
    Transformer(int d_model, int num_layers, int num_heads, int d_ff);
    Matrix forward(const Matrix& x);
    Matrix backward(const Matrix& grad_output);
    void update_weights(float learning_rate);
    float compute_loss(const Matrix& output, const Matrix& target);
    Matrix compute_loss_gradient(const Matrix& output, const Matrix& target);

private:
    int d_model;
    std::vector<std::unique_ptr<TransformerLayer>> layers;
    
    // 存储前向传播的中间结果
    Matrix last_input;
    Matrix last_pos_encoding;
    std::vector<Matrix> layer_outputs;
    
    Matrix positional_encoding(const Matrix& x);
    Matrix positional_encoding_backward(const Matrix& grad_output);
}; 