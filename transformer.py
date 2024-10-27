import tensorflow as tf
from tensorflow import keras
import numpy as np

# Transformer模型实现
class TransformerModel(keras.Model):
    def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, 
                 target_vocab_size, pe_input, pe_target, rate=0.1):
        super(TransformerModel, self).__init__()

        # 初始化编码器
        self.encoder = Encoder(num_layers, d_model, num_heads, dff,
                               input_vocab_size, pe_input, rate)

        # 初始化解码器
        self.decoder = Decoder(num_layers, d_model, num_heads, dff,
                               target_vocab_size, pe_target, rate)

        # 最终的线性层，用于生成目标词汇表大小的输出
        self.final_layer = tf.keras.layers.Dense(target_vocab_size)

    def call(self, inputs, targets, training):
        # inputs.shape == (batch_size, input_seq_len)
        # targets.shape == (batch_size, target_seq_len)

        # 创建编码器和解码器的填充掩码
        enc_padding_mask = create_padding_mask(inputs)
        dec_padding_mask = create_padding_mask(inputs)

        # 创建解码器的前瞻掩码，防止关注到未来的标记
        look_ahead_mask = create_look_ahead_mask(tf.shape(targets)[1])
        dec_target_padding_mask = create_padding_mask(targets)
        combined_mask = tf.maximum(dec_target_padding_mask, look_ahead_mask)

        # 编码器输出
        enc_output = self.encoder(inputs, training, enc_padding_mask)  # (batch_size, inp_seq_len, d_model)

        # 解码器输出
        dec_output = self.decoder(targets, enc_output, training, combined_mask, dec_padding_mask)

        # 最终输出
        final_output = self.final_layer(dec_output)  # (batch_size, tar_seq_len, target_vocab_size)

        return final_output

class Encoder(tf.keras.layers.Layer):
    def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, maximum_position_encoding, rate=0.1):
        super(Encoder, self).__init__()

        self.d_model = d_model
        self.num_layers = num_layers

        # 输入嵌入层
        self.embedding = tf.keras.layers.Embedding(input_vocab_size, d_model)
        # 位置编码
        self.pos_encoding = positional_encoding(maximum_position_encoding, self.d_model)

        # 创建多个编码器层
        self.enc_layers = [EncoderLayer(d_model, num_heads, dff, rate) 
                           for _ in range(num_layers)]

        self.dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, training, mask):
        seq_len = tf.shape(x)[1]

        # 添加嵌入和位置编码
        x = self.embedding(x)  # (batch_size, input_seq_len, d_model)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))  # 缩放嵌入
        x += self.pos_encoding[:, :seq_len, :]

        x = self.dropout(x, training=training)

        # 通过多个编码器层
        for i in range(self.num_layers):
            x = self.enc_layers[i](x, training, mask)

        return x  # (batch_size, input_seq_len, d_model)

class Decoder(tf.keras.layers.Layer):
    def __init__(self, num_layers, d_model, num_heads, dff, target_vocab_size, maximum_position_encoding, rate=0.1):
        super(Decoder, self).__init__()

        self.d_model = d_model
        self.num_layers = num_layers

        # 目标序列的嵌入层
        self.embedding = tf.keras.layers.Embedding(target_vocab_size, d_model)
        # 位置编码
        self.pos_encoding = positional_encoding(maximum_position_encoding, d_model)

        # 创建多个解码器层
        self.dec_layers = [DecoderLayer(d_model, num_heads, dff, rate) 
                           for _ in range(num_layers)]
        self.dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
        seq_len = tf.shape(x)[1]
        attention_weights = {}

        # 添加嵌入和位置编码
        x = self.embedding(x)  # (batch_size, target_seq_len, d_model)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))  # 缩放嵌入
        x += self.pos_encoding[:, :seq_len, :]

        x = self.dropout(x, training=training)

        # 通过多个解码器层
        for i in range(self.num_layers):
            x, block1, block2 = self.dec_layers[i](x, enc_output, training,
                                                   look_ahead_mask, padding_mask)

            attention_weights[f'decoder_layer{i+1}_block1'] = block1
            attention_weights[f'decoder_layer{i+1}_block2'] = block2

        return x, attention_weights

# 辅助函数
def get_angles(pos, i, d_model):
    # 计算位置编码的角度
    angle_rates = 1 / np.power(10000, (2 * (i//2)) / np.float32(d_model))
    return pos * angle_rates

def positional_encoding(position, d_model):
    # 生成位置编码
    angle_rads = get_angles(np.arange(position)[:, np.newaxis],
                            np.arange(d_model)[np.newaxis, :],
                            d_model)

    # 应用正弦和余弦函数
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])

    pos_encoding = angle_rads[np.newaxis, ...]

    return tf.cast(pos_encoding, dtype=tf.float32)

def create_padding_mask(seq):
    # 创建填充掩码，用于遮蔽填充标记
    seq = tf.cast(tf.math.equal(seq, 0), tf.float32)
    return seq[:, tf.newaxis, tf.newaxis, :]  # (batch_size, 1, 1, seq_len)

def create_look_ahead_mask(size):
    # 创建前瞻掩码，用于遮蔽未来的标记
    mask = 1 - tf.linalg.band_part(tf.ones((size, size)), -1, 0)
    return mask  # (seq_len, seq_len)

# 原理解释：
# 1. TransformerModel: 整体架构包含编码器、解码器和最终输出层。
#    - 编码器处理输入序列
#    - 解码器利用编码器输出和之前的输出生成目标序列
#    - 最终线性层将解码器输出映射到目标词汇表大小

# 2. Encoder: 将输入序列编码为连续表示
#    - 嵌入层将输入标记转换为向量
#    - 位置编码添加序列中的位置信息
#    - 多个编码器层堆叠，每层包含自注意力机制和前馈网络

# 3. Decoder: 生成输出序列
#    - 结构类似编码器，但包含额外的注意力层来关注编码器输出
#    - 使用掩码来防止关注到未来的标记

# 4. 位置编码（Positional Encoding）: 
#    - 使用正弦和余弦函数生成，为模型提供序列中的位置信息
#    - 允许模型学习相对位置关系

# 5. 掩码（Masking）:
#    - 填充掩码用于忽略序列中的填充标记
#    - 前瞻掩码防止解码器在生成过程中看到未来的标记

# 6. 注意力机制：
#    - 允许模型关注输入的不同部分
#    - 多头注意力机制在不同的表示子空间中并行地执行注意力计算

# 这个实现展示了Transformer的核心组件和工作原理。在实际应用中，还需要实现具体的EncoderLayer和DecoderLayer，
# 以及训练循环、损失函数和优化器。Transformer的强大之处在于其并行处理能力和捕捉长距离依赖的能力。


# 在文件末尾添加以下代码

def demo_transformer():
    # 设置模型参数
    num_layers = 4
    d_model = 128
    num_heads = 8
    dff = 512
    input_vocab_size = 8000
    target_vocab_size = 8000
    pe_input = 10000
    pe_target = 6000

    # 初始化模型
    transformer = TransformerModel(num_layers, d_model, num_heads, dff,
                                   input_vocab_size, target_vocab_size,
                                   pe_input, pe_target)

    # 创建一些示例输入
    temp_input = tf.random.uniform((64, 62))  # (batch_size, input_seq_len)
    temp_target = tf.random.uniform((64, 26))  # (batch_size, target_seq_len)

    # 运行模型
    fn_out = transformer(temp_input, temp_target, training=False)

    print(f"输出形状: {fn_out.shape}")  # (batch_size, tar_seq_len, target_vocab_size)

if __name__ == "__main__":
    demo_transformer()
