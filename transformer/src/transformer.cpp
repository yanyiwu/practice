#include "transformer.hpp"
#include <algorithm>
#include <numeric>
#include <cmath>

// Helper function for Xavier initialization
float xavier_init(int fan_in, int fan_out) {
    float limit = std::sqrt(6.0f / (fan_in + fan_out));
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dist(-limit, limit);
    return dist(gen);
}

// MultiHeadAttention implementation
MultiHeadAttention::MultiHeadAttention(int d_model, int num_heads) 
    : d_model(d_model), num_heads(num_heads), d_k(d_model / num_heads) {
    initialize_weights();
}

void MultiHeadAttention::initialize_weights() {
    // Initialize weight matrices with Xavier initialization
    W_q = Matrix(d_model, std::vector<float>(d_model));
    W_k = Matrix(d_model, std::vector<float>(d_model));
    W_v = Matrix(d_model, std::vector<float>(d_model));
    W_o = Matrix(d_model, std::vector<float>(d_model));
    
    // Initialize gradient matrices
    grad_W_q = Matrix(d_model, std::vector<float>(d_model));
    grad_W_k = Matrix(d_model, std::vector<float>(d_model));
    grad_W_v = Matrix(d_model, std::vector<float>(d_model));
    grad_W_o = Matrix(d_model, std::vector<float>(d_model));

    for (int i = 0; i < d_model; ++i) {
        for (int j = 0; j < d_model; ++j) {
            W_q[i][j] = xavier_init(d_model, d_model);
            W_k[i][j] = xavier_init(d_model, d_model);
            W_v[i][j] = xavier_init(d_model, d_model);
            W_o[i][j] = xavier_init(d_model, d_model);
        }
    }
}

Matrix MultiHeadAttention::scaled_dot_product_attention(
    const Matrix& Q,
    const Matrix& K,
    const Matrix& V) {
    
    int seq_len = Q.size();
    Matrix scores(seq_len, std::vector<float>(seq_len));
    
    const float scale = 1.0f / std::sqrt(d_k);  // Pre-compute scaling factor
    
    // Calculate attention scores with improved numerical stability
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < seq_len; ++j) {
            float sum = 0.0f;
            for (int k = 0; k < d_k; ++k) {
                // Apply scaling during dot product to prevent large values
                sum += (Q[i][k] * scale) * K[j][k];
            }
            scores[i][j] = sum;
        }
    }
    
    // Store for backward pass
    last_attention_scores = scores;
    
    // Apply softmax with improved numerical stability
    Matrix softmax_scores(seq_len, std::vector<float>(seq_len));
    for (int i = 0; i < seq_len; ++i) {
        // Find max value for numerical stability
        float max_val = -std::numeric_limits<float>::infinity();
        for (int j = 0; j < seq_len; ++j) {
            max_val = std::max(max_val, scores[i][j]);
        }
        
        // Compute exp and sum
        float sum = 0.0f;
        for (int j = 0; j < seq_len; ++j) {
            softmax_scores[i][j] = std::exp(scores[i][j] - max_val);
            sum += softmax_scores[i][j];
        }
        
        // Normalize
        const float eps = 1e-6f;
        sum = std::max(sum, eps);  // Prevent division by zero
        for (int j = 0; j < seq_len; ++j) {
            softmax_scores[i][j] /= sum;
        }
    }
    
    // Calculate attention output with improved numerical stability
    Matrix output(seq_len, std::vector<float>(d_k));
    for (int i = 0; i < seq_len; ++i) {
        for (int k = 0; k < d_k; ++k) {
            float sum = 0.0f;
            for (int j = 0; j < seq_len; ++j) {
                sum += softmax_scores[i][j] * V[j][k];
            }
            // Clip output values to prevent explosion
            output[i][k] = std::max(std::min(sum, 5.0f), -5.0f);
        }
    }
    
    return output;
}

Matrix MultiHeadAttention::scaled_dot_product_attention_backward(const Matrix& grad_output) {
    int seq_len = grad_output.size();
    Matrix grad_scores(seq_len, std::vector<float>(seq_len));
    Matrix grad_v(seq_len, std::vector<float>(d_k));
    Matrix grad_q(seq_len, std::vector<float>(d_k));
    Matrix grad_k(seq_len, std::vector<float>(d_k));
    
    // Gradient w.r.t. attention scores
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < seq_len; ++j) {
            float sum = 0.0f;
            for (int k = 0; k < d_k; ++k) {
                sum += grad_output[i][k] * last_value[j][k];
            }
            grad_scores[i][j] = sum;
        }
    }
    
    // Gradient w.r.t. softmax
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < seq_len; ++j) {
            float softmax = last_attention_scores[i][j];
            for (int k = 0; k < seq_len; ++k) {
                float delta = (j == k) ? 1.0f : 0.0f;
                grad_scores[i][j] *= softmax * (delta - last_attention_scores[i][k]);
            }
        }
    }
    
    // Scale gradients
    float scale = 1.0f / std::sqrt(d_k);
    for (auto& row : grad_scores) {
        for (auto& val : row) {
            val *= scale;
        }
    }
    
    // Gradient w.r.t. Q, K, V
    for (int i = 0; i < seq_len; ++i) {
        for (int k = 0; k < d_k; ++k) {
            for (int j = 0; j < seq_len; ++j) {
                grad_q[i][k] += grad_scores[i][j] * last_key[j][k];
                grad_k[j][k] += grad_scores[i][j] * last_query[i][k];
                grad_v[j][k] += last_attention_scores[i][j] * grad_output[i][k];
            }
        }
    }
    
    return grad_q;  // Return gradient w.r.t. input query
}

Matrix MultiHeadAttention::forward(
    const Matrix& query,
    const Matrix& key,
    const Matrix& value) {
    
    // Store inputs for backward pass
    last_query = query;
    last_key = key;
    last_value = value;
    
    int seq_len = query.size();
    Matrix output(seq_len, std::vector<float>(d_model, 0.0f));
    
    // Split into heads and process each head
    for (int h = 0; h < num_heads; ++h) {
        // Project queries, keys, and values with improved numerical stability
        Matrix Q(seq_len, std::vector<float>(d_k));
        Matrix K(seq_len, std::vector<float>(d_k));
        Matrix V(seq_len, std::vector<float>(d_k));
        
        // Project input for this head with scaling factor
        const float proj_scale = 1.0f / std::sqrt(d_model);
        for (int i = 0; i < seq_len; ++i) {
            for (int j = 0; j < d_k; ++j) {
                float q_sum = 0.0f;
                float k_sum = 0.0f;
                float v_sum = 0.0f;
                
                for (int k = 0; k < d_model; ++k) {
                    q_sum += query[i][k] * W_q[h * d_k + j][k] * proj_scale;
                    k_sum += key[i][k] * W_k[h * d_k + j][k] * proj_scale;
                    v_sum += value[i][k] * W_v[h * d_k + j][k] * proj_scale;
                }
                
                // Clip projected values
                Q[i][j] = std::max(std::min(q_sum, 5.0f), -5.0f);
                K[i][j] = std::max(std::min(k_sum, 5.0f), -5.0f);
                V[i][j] = std::max(std::min(v_sum, 5.0f), -5.0f);
            }
        }
        
        // Calculate attention for this head
        auto head_output = scaled_dot_product_attention(Q, K, V);
        
        // Concatenate heads with improved numerical stability
        for (int i = 0; i < seq_len; ++i) {
            for (int j = 0; j < d_k; ++j) {
                output[i][h * d_k + j] = head_output[i][j];
            }
        }
    }
    
    // Store output for backward pass
    last_attention_output = output;
    
    // Final projection with improved numerical stability
    Matrix final_output(seq_len, std::vector<float>(d_model));
    const float out_scale = 1.0f / std::sqrt(d_model);
    
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_model; ++j) {
            float sum = 0.0f;
            for (int k = 0; k < d_model; ++k) {
                sum += output[i][k] * W_o[j][k] * out_scale;
            }
            // Clip final output
            final_output[i][j] = std::max(std::min(sum, 5.0f), -5.0f);
        }
    }
    
    return final_output;
}

Matrix MultiHeadAttention::backward(const Matrix& grad_output) {
    int seq_len = grad_output.size();
    Matrix grad_attention(seq_len, std::vector<float>(d_model));
    
    // Gradient w.r.t. attention output
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_model; ++j) {
            for (int k = 0; k < d_model; ++k) {
                grad_attention[i][k] += grad_output[i][j] * W_o[j][k];
                grad_W_o[j][k] += grad_output[i][j] * last_attention_output[i][k];
            }
        }
    }
    
    // Gradient for each attention head
    Matrix grad_query(seq_len, std::vector<float>(d_model));
    for (int h = 0; h < num_heads; ++h) {
        Matrix head_grad(seq_len, std::vector<float>(d_k));
        
        // Extract gradient for this head
        for (int i = 0; i < seq_len; ++i) {
            for (int j = 0; j < d_k; ++j) {
                head_grad[i][j] = grad_attention[i][h * d_k + j];
            }
        }
        
        // Backward pass through attention mechanism
        auto grad_qkv = scaled_dot_product_attention_backward(head_grad);
        
        // Accumulate gradients for the projection matrices
        for (int i = 0; i < seq_len; ++i) {
            for (int j = 0; j < d_k; ++j) {
                for (int k = 0; k < d_model; ++k) {
                    grad_query[i][k] += grad_qkv[i][j] * W_q[h * d_k + j][k];
                    grad_W_q[h * d_k + j][k] += grad_qkv[i][j] * last_query[i][k];
                }
            }
        }
    }
    
    return grad_query;
}

void MultiHeadAttention::update_weights(float learning_rate) {
    // Update all weights using their gradients
    for (int i = 0; i < d_model; ++i) {
        for (int j = 0; j < d_model; ++j) {
            W_q[i][j] -= learning_rate * grad_W_q[i][j];
            W_k[i][j] -= learning_rate * grad_W_k[i][j];
            W_v[i][j] -= learning_rate * grad_W_v[i][j];
            W_o[i][j] -= learning_rate * grad_W_o[i][j];
            
            // Reset gradients
            grad_W_q[i][j] = 0.0f;
            grad_W_k[i][j] = 0.0f;
            grad_W_v[i][j] = 0.0f;
            grad_W_o[i][j] = 0.0f;
        }
    }
}

// FeedForward implementation
FeedForward::FeedForward(int d_model, int d_ff) : d_model(d_model), d_ff(d_ff) {
    initialize_weights();
}

void FeedForward::initialize_weights() {
    // Initialize weights with Xavier initialization
    W1 = Matrix(d_ff, std::vector<float>(d_model));
    W2 = Matrix(d_model, std::vector<float>(d_ff));
    b1 = std::vector<float>(d_ff, 0.0f);
    b2 = std::vector<float>(d_model, 0.0f);
    
    for (int i = 0; i < d_ff; ++i) {
        for (int j = 0; j < d_model; ++j) {
            W1[i][j] = xavier_init(d_model, d_ff);
        }
    }
    
    for (int i = 0; i < d_model; ++i) {
        for (int j = 0; j < d_ff; ++j) {
            W2[i][j] = xavier_init(d_ff, d_model);
        }
    }
}

Matrix FeedForward::forward(const Matrix& x) {
    // Store input for backward pass
    last_input = x;
    
    int seq_len = x.size();
    Matrix hidden(seq_len, std::vector<float>(d_ff));
    Matrix output(seq_len, std::vector<float>(d_model));
    
    // First layer with ReLU
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_ff; ++j) {
            float sum = b1[j];
            for (int k = 0; k < d_model; ++k) {
                sum += W1[j][k] * x[i][k];
            }
            hidden[i][j] = std::max(0.0f, sum); // ReLU activation
        }
    }
    
    // Store hidden layer output for backward pass
    last_hidden = hidden;
    
    // Second layer
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_model; ++j) {
            float sum = b2[j];
            for (int k = 0; k < d_ff; ++k) {
                sum += W2[j][k] * hidden[i][k];
            }
            output[i][j] = sum;
        }
    }
    
    return output;
}

// TransformerLayer implementation
TransformerLayer::TransformerLayer(int d_model, int num_heads, int d_ff) {
    self_attention = std::make_unique<MultiHeadAttention>(d_model, num_heads);
    feed_forward = std::make_unique<FeedForward>(d_model, d_ff);
}

Matrix TransformerLayer::layer_norm(const Matrix& x) {
    int seq_len = x.size();
    int feat_dim = x[0].size();
    Matrix output = x;
    
    const float eps = 1e-5f;  // 增加epsilon值以提高数值稳定性
    
    for (int i = 0; i < seq_len; ++i) {
        // Calculate mean
        float mean = 0.0f;
        for (int j = 0; j < feat_dim; ++j) {
            mean += x[i][j];
        }
        mean /= feat_dim;
        
        // Calculate variance
        float var = 0.0f;
        for (int j = 0; j < feat_dim; ++j) {
            float diff = x[i][j] - mean;
            var += diff * diff;
        }
        var = std::max(var / feat_dim, eps);  // 确保方差不会太小
        
        // Normalize
        float std = std::sqrt(var);
        for (int j = 0; j < feat_dim; ++j) {
            output[i][j] = (x[i][j] - mean) / std;
        }
    }
    
    return output;
}

Matrix TransformerLayer::forward(const Matrix& x) {
    // Store input for backward pass
    last_input = x;
    
    // Self attention
    auto attention_output = self_attention->forward(x, x, x);
    last_attention_output = attention_output;
    
    // First Add & Norm
    auto norm1 = layer_norm(attention_output);
    last_norm1_output = norm1;
    
    // Add residual connection
    for (size_t i = 0; i < x.size(); ++i) {
        for (size_t j = 0; j < x[0].size(); ++j) {
            norm1[i][j] += x[i][j];
        }
    }
    
    // Feed forward
    auto ff_output = feed_forward->forward(norm1);
    last_ff_output = ff_output;
    
    // Second Add & Norm
    auto norm2 = layer_norm(ff_output);
    last_norm2_output = norm2;
    
    // Add residual connection
    for (size_t i = 0; i < x.size(); ++i) {
        for (size_t j = 0; j < x[0].size(); ++j) {
            norm2[i][j] += norm1[i][j];
        }
    }
    
    return norm2;
}

// Transformer implementation
Transformer::Transformer(int d_model, int num_layers, int num_heads, int d_ff) : d_model(d_model) {
    for (int i = 0; i < num_layers; ++i) {
        layers.push_back(std::make_unique<TransformerLayer>(d_model, num_heads, d_ff));
    }
}

std::vector<std::vector<float>> Transformer::positional_encoding(const std::vector<std::vector<float>>& x) {
    int seq_len = x.size();
    std::vector<std::vector<float>> pos_encoding = x;
    
    for (int pos = 0; pos < seq_len; ++pos) {
        for (int i = 0; i < d_model; i += 2) {
            float angle = pos / std::pow(10000, (2.0f * i) / d_model);
            pos_encoding[pos][i] += std::sin(angle);
            if (i + 1 < d_model) {
                pos_encoding[pos][i + 1] += std::cos(angle);
            }
        }
    }
    
    return pos_encoding;
}

Matrix Transformer::forward(const Matrix& x) {
    // Store input for backward pass
    last_input = x;
    
    // Apply positional encoding
    auto pos_encoded = positional_encoding(x);
    last_pos_encoding = pos_encoded;
    
    // Clear previous layer outputs
    layer_outputs.clear();
    layer_outputs.push_back(pos_encoded);
    
    // Forward through layers
    auto output = pos_encoded;
    for (const auto& layer : layers) {
        output = layer->forward(output);
        layer_outputs.push_back(output);
    }
    
    return output;
}

Matrix Transformer::compute_loss_gradient(const Matrix& output, const Matrix& target) {
    int seq_len = output.size();
    int d_model = output[0].size();
    Matrix gradient(seq_len, std::vector<float>(d_model));
    
    // MSE loss gradient
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_model; ++j) {
            gradient[i][j] = 2.0f * (output[i][j] - target[i][j]) / (seq_len * d_model);
        }
    }
    
    return gradient;
}

Matrix Transformer::backward(const Matrix& grad_output) {
    Matrix gradient = grad_output;
    
    // Backward through layers in reverse order
    for (int i = layers.size() - 1; i >= 0; --i) {
        gradient = layers[i]->backward(gradient);
    }
    
    // Backward through positional encoding
    gradient = positional_encoding_backward(gradient);
    
    return gradient;
}

Matrix Transformer::positional_encoding_backward(const Matrix& grad_output) {
    // Since positional encoding is just addition, gradient flows straight through
    return grad_output;
}

void Transformer::update_weights(float learning_rate) {
    for (auto& layer : layers) {
        layer->update_weights(learning_rate);
    }
}

// TransformerLayer implementation
Matrix TransformerLayer::backward(const Matrix& grad_output) {
    // Store input gradient for this layer
    Matrix gradient = grad_output;
    
    // Backward through second Add & Norm
    Matrix grad_ff = gradient;
    gradient = layer_norm_backward(grad_ff, last_ff_output);
    
    // Add residual gradient
    for (size_t i = 0; i < gradient.size(); ++i) {
        for (size_t j = 0; j < gradient[0].size(); ++j) {
            gradient[i][j] += grad_ff[i][j];
        }
    }
    
    // Backward through feed forward
    gradient = feed_forward->backward(gradient);
    
    // Backward through first Add & Norm
    Matrix grad_attention = gradient;
    gradient = layer_norm_backward(grad_attention, last_attention_output);
    
    // Add residual gradient
    for (size_t i = 0; i < gradient.size(); ++i) {
        for (size_t j = 0; j < gradient[0].size(); ++j) {
            gradient[i][j] += grad_attention[i][j];
        }
    }
    
    // Backward through self attention
    gradient = self_attention->backward(gradient);
    
    return gradient;
}

Matrix TransformerLayer::layer_norm_backward(const Matrix& grad_output, const Matrix& last_input) {
    int seq_len = grad_output.size();
    int feat_dim = grad_output[0].size();
    Matrix gradient(seq_len, std::vector<float>(feat_dim));
    
    const float eps = 1e-5f;
    
    for (int i = 0; i < seq_len; ++i) {
        // Calculate statistics from forward pass
        float mean = 0.0f;
        for (int j = 0; j < feat_dim; ++j) {
            mean += last_input[i][j];
        }
        mean /= feat_dim;
        
        float var = 0.0f;
        for (int j = 0; j < feat_dim; ++j) {
            float diff = last_input[i][j] - mean;
            var += diff * diff;
        }
        var = std::max(var / feat_dim, eps);
        float std = std::sqrt(var);
        
        // Compute gradients
        std::vector<float> grad_var(feat_dim);
        float grad_mean = 0.0f;
        
        for (int j = 0; j < feat_dim; ++j) {
            float x_centered = last_input[i][j] - mean;
            grad_var[j] = grad_output[i][j] * x_centered * (-0.5f) * std::pow(var, -1.5f);
            grad_mean -= grad_output[i][j] / std;
        }
        
        grad_mean /= feat_dim;
        
        // Combine gradients
        for (int j = 0; j < feat_dim; ++j) {
            float x_centered = last_input[i][j] - mean;
            gradient[i][j] = grad_output[i][j] / std + 
                            grad_var[j] * 2.0f * x_centered / feat_dim +
                            grad_mean;
            
            // Add gradient clipping
            gradient[i][j] = std::max(std::min(gradient[i][j], 1.0f), -1.0f);
        }
    }
    
    return gradient;
}

void TransformerLayer::update_weights(float learning_rate) {
    self_attention->update_weights(learning_rate);
    feed_forward->update_weights(learning_rate);
}

// FeedForward backward implementation
Matrix FeedForward::backward(const Matrix& grad_output) {
    int seq_len = grad_output.size();
    Matrix gradient(seq_len, std::vector<float>(d_model));
    
    // Initialize gradient matrices if not done
    if (grad_W1.empty()) {
        grad_W1 = Matrix(d_ff, std::vector<float>(d_model));
        grad_W2 = Matrix(d_model, std::vector<float>(d_ff));
        grad_b1 = std::vector<float>(d_ff);
        grad_b2 = std::vector<float>(d_model);
    }
    
    // Backward through second layer
    Matrix grad_hidden(seq_len, std::vector<float>(d_ff));
    
    for (int i = 0; i < seq_len; ++i) {
        // Gradient w.r.t. bias
        for (int j = 0; j < d_model; ++j) {
            grad_b2[j] += grad_output[i][j];
        }
        
        // Gradient w.r.t. weights and hidden layer
        for (int j = 0; j < d_model; ++j) {
            for (int k = 0; k < d_ff; ++k) {
                grad_W2[j][k] += grad_output[i][j] * last_hidden[i][k];
                grad_hidden[i][k] += grad_output[i][j] * W2[j][k];
            }
        }
    }
    
    // Backward through ReLU
    for (int i = 0; i < seq_len; ++i) {
        for (int j = 0; j < d_ff; ++j) {
            grad_hidden[i][j] *= (last_hidden[i][j] > 0.0f) ? 1.0f : 0.0f;
        }
    }
    
    // Backward through first layer
    for (int i = 0; i < seq_len; ++i) {
        // Gradient w.r.t. bias
        for (int j = 0; j < d_ff; ++j) {
            grad_b1[j] += grad_hidden[i][j];
        }
        
        // Gradient w.r.t. weights and input
        for (int j = 0; j < d_ff; ++j) {
            for (int k = 0; k < d_model; ++k) {
                grad_W1[j][k] += grad_hidden[i][j] * last_input[i][k];
                gradient[i][k] += grad_hidden[i][j] * W1[j][k];
            }
        }
    }
    
    return gradient;
}

void FeedForward::update_weights(float learning_rate) {
    // Update weights and biases
    for (int i = 0; i < d_ff; ++i) {
        for (int j = 0; j < d_model; ++j) {
            W1[i][j] -= learning_rate * grad_W1[i][j];
            grad_W1[i][j] = 0.0f;  // Reset gradient
        }
        b1[i] -= learning_rate * grad_b1[i];
        grad_b1[i] = 0.0f;  // Reset gradient
    }
    
    for (int i = 0; i < d_model; ++i) {
        for (int j = 0; j < d_ff; ++j) {
            W2[i][j] -= learning_rate * grad_W2[i][j];
            grad_W2[i][j] = 0.0f;  // Reset gradient
        }
        b2[i] -= learning_rate * grad_b2[i];
        grad_b2[i] = 0.0f;  // Reset gradient
    }
} 



// hi my name is nobody don't add this to your repo :)
//Wild And Free