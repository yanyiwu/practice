import tensorflow as tf
from tensorflow import keras
import numpy as np

# 首先定义所有辅助函数
def get_angles(pos, i, d_model):
    angle_rates = 1 / np.power(10000, (2 * (i//2)) / np.float32(d_model))
    return pos * angle_rates

def positional_encoding(position, d_model):
    angle_rads = get_angles(np.arange(position)[:, np.newaxis],
                            np.arange(d_model)[np.newaxis, :],
                            d_model)
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
    pos_encoding = angle_rads[np.newaxis, ...]
    return tf.cast(pos_encoding, dtype=tf.float32)

def create_padding_mask(seq):
    # seq shape: (batch_size, seq_len)
    seq = tf.cast(tf.math.equal(seq, 0), tf.float32)
    # seq shape: (batch_size, seq_len)
    r = seq[:, tf.newaxis, tf.newaxis, :]
    # r shape: (batch_size, 1, 1, seq_len)
    return r

def create_look_ahead_mask(size):
    mask = 1 - tf.linalg.band_part(tf.ones((size, size)), -1, 0)
    return mask

def scaled_dot_product_attention(q, k, v, mask):
    # q shape: (batch_size, num_heads, seq_len_q, depth)
    # k shape: (batch_size, num_heads, seq_len_k, depth)
    # v shape: (batch_size, num_heads, seq_len_v, depth)    
    matmul_qk = tf.matmul(q, k, transpose_b=True)
    # matmul_qk shape: (batch_size, num_heads, seq_len_q, seq_len_k)
    dk = tf.cast(tf.shape(k)[-1], tf.float32)
    # dk shape: depth
    scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)
    # scaled_attention_logits shape: (batch_size, num_heads, seq_len_q, seq_len_k)
    if mask is not None:
        scaled_attention_logits += (mask * -1e9)  
    # scaled_attention_logits shape: (batch_size, num_heads, seq_len_q, seq_len_k)
    attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)
    # attention_weights shape: (batch_size, num_heads, seq_len_q, seq_len_k)
    output = tf.matmul(attention_weights, v)
    # output shape: (batch_size, num_heads, seq_len_q, depth)
    return output, attention_weights

def point_wise_feed_forward_network(d_model, dff):
    return tf.keras.Sequential([
        tf.keras.layers.Dense(dff, activation='relu'),
        tf.keras.layers.Dense(d_model)
    ])

# 然后定义所有层和模型类
class MultiHeadAttention(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.num_heads = num_heads
        self.d_model = d_model
        assert d_model % self.num_heads == 0
        self.depth = d_model // self.num_heads
        self.wq = tf.keras.layers.Dense(d_model)
        self.wk = tf.keras.layers.Dense(d_model)
        self.wv = tf.keras.layers.Dense(d_model)
        self.dense = tf.keras.layers.Dense(d_model)

    def split_heads(self, x, batch_size):
        # x shape: (batch_size, seq_len, d_model)   
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        # x shape: (batch_size, seq_len, num_heads,depth)
        x = tf.transpose(x, perm=[0, 2, 1, 3])
        # x shape: (batch_size, num_heads, seq_len, depth)  
        return x

    def call(self, v, k, q, mask):
        batch_size = tf.shape(q)[0]
        # q shape: (batch_size, seq_len, d_model)
        q = self.wq(q)
        # q shape: (batch_size, seq_len, d_model)
        k = self.wk(k)
        # k shape: (batch_size, seq_len, d_model)
        v = self.wv(v)
        # v shape: (batch_size, seq_len, d_model)
        q = self.split_heads(q, batch_size)
        # q shape: (batch_size, num_heads, seq_len_q, depth)
        k = self.split_heads(k, batch_size)
        # k shape: (batch_size, num_heads, seq_len_k, depth)
        v = self.split_heads(v, batch_size)
        # v shape: (batch_size, num_heads, seq_len_v, depth)
        scaled_attention, attention_weights = scaled_dot_product_attention(q, k, v, mask)
        # scaled_attention shape: (batch_size, num_heads, seq_len_q, depth)
        # attention_weights shape: (batch_size, num_heads, seq_len_q, seq_len_k)
        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])
        # scaled_attention shape: (batch_size, seq_len_q, num_heads, depth)
        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))
        # concat_attention shape: (batch_size, seq_len_q, d_model)
        output = self.dense(concat_attention)
        # output shape: (batch_size, seq_len_q, d_model)
        return output, attention_weights

class EncoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super(EncoderLayer, self).__init__()
        self.mha = MultiHeadAttention(d_model, num_heads)
        self.ffn = point_wise_feed_forward_network(d_model, dff)
        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)

    def call(self, x, training, mask):
        # x shape: (batch_size, input_seq_len, d_model)
        attn_output, _ = self.mha(x, x, x, mask)
        # attn_output shape: (batch_size, input_seq_len, d_model)
        attn_output = self.dropout1(attn_output, training=training)
        # attn_output shape: (batch_size, input_seq_len, d_model)
        out1 = self.layernorm1(x + attn_output)
        # out1 shape: (batch_size, input_seq_len, d_model)
        ffn_output = self.ffn(out1) 
        # ffn_output shape: (batch_size, input_seq_len, d_model)
        ffn_output = self.dropout2(ffn_output, training=training)
        # ffn_output shape: (batch_size, input_seq_len, d_model)
        out2 = self.layernorm2(out1 + ffn_output)
        # out2 shape: (batch_size, input_seq_len, d_model)
        return out2

class DecoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super(DecoderLayer, self).__init__()
        self.mha1 = MultiHeadAttention(d_model, num_heads)
        self.mha2 = MultiHeadAttention(d_model, num_heads)
        self.ffn = point_wise_feed_forward_network(d_model, dff)
        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm3 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)
        self.dropout3 = tf.keras.layers.Dropout(rate)

    def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
        attn1, attn_weights_block1 = self.mha1(x, x, x, look_ahead_mask)
        attn1 = self.dropout1(attn1, training=training)
        out1 = self.layernorm1(attn1 + x)
        attn2, attn_weights_block2 = self.mha2(enc_output, enc_output, out1, padding_mask)
        attn2 = self.dropout2(attn2, training=training)
        out2 = self.layernorm2(attn2 + out1)
        ffn_output = self.ffn(out2)
        ffn_output = self.dropout3(ffn_output, training=training)
        out3 = self.layernorm3(ffn_output + out2)
        return out3, attn_weights_block1, attn_weights_block2

class Encoder(tf.keras.layers.Layer):
    def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, maximum_position_encoding, rate=0.1):
        super(Encoder, self).__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        self.embedding = tf.keras.layers.Embedding(input_vocab_size, d_model)
        self.pos_encoding = positional_encoding(maximum_position_encoding, self.d_model)
        self.enc_layers = [EncoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]
        self.dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, training=None, mask=None):
        # x shape: (batch_size, input_seq_len)
        seq_len = tf.shape(x)[1]
        # seq_len shape: input_seq_len
        x = self.embedding(x)
        # x shape: (batch_size, input_seq_len, d_model) 
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        # x shape: (batch_size, input_seq_len, d_model) 
        x += self.pos_encoding[:, :seq_len, :]
        # x shape: (batch_size, input_seq_len, d_model)
        x = self.dropout(x, training=training)
        # x shape: (batch_size, input_seq_len, d_model)
        for i in range(self.num_layers):
            x = self.enc_layers[i](x, training=training, mask=mask)
        # x shape: (batch_size, input_seq_len, d_model)
        return x

class Decoder(tf.keras.layers.Layer):
    def __init__(self, num_layers, d_model, num_heads, dff, target_vocab_size, maximum_position_encoding, rate=0.1):
        super(Decoder, self).__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        self.embedding = tf.keras.layers.Embedding(target_vocab_size, d_model)
        self.pos_encoding = positional_encoding(maximum_position_encoding, d_model)
        self.dec_layers = [DecoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]
        self.dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, enc_output, training=None, look_ahead_mask=None, padding_mask=None):
        seq_len = tf.shape(x)[1]
        attention_weights = {}
        x = self.embedding(x)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        x += self.pos_encoding[:, :seq_len, :]
        x = self.dropout(x, training=training)
        for i in range(self.num_layers):
            x, block1, block2 = self.dec_layers[i](x, enc_output, training=training, 
                                                   look_ahead_mask=look_ahead_mask, 
                                                   padding_mask=padding_mask)
            attention_weights[f'decoder_layer{i+1}_block1'] = block1
            attention_weights[f'decoder_layer{i+1}_block2'] = block2
        return x, attention_weights

class TransformerModel(keras.Model):
    def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size, 
                 target_vocab_size, pe_input, pe_target, rate=0.1):
        super(TransformerModel, self).__init__()
        self.encoder = Encoder(num_layers, d_model, num_heads, dff,
                               input_vocab_size, pe_input, rate)
        self.decoder = Decoder(num_layers, d_model, num_heads, dff,
                               target_vocab_size, pe_target, rate)
        self.final_layer = tf.keras.layers.Dense(target_vocab_size)

    def call(self, inputs, training=None, mask=None):
        inp, tar = inputs
        # inp shape: (batch_size, input_seq_len)
        # tar shape: (batch_size, target_seq_len)   

        enc_padding_mask = create_padding_mask(inp)
        # enc_padding_mask shape: (batch_size, 1, 1, input_seq_len)
        enc_output = self.encoder(inp, training=training, mask=enc_padding_mask)
        # enc_output shape: (batch_size, input_seq_len, d_model)

        dec_padding_mask = create_padding_mask(inp)
        # dec_padding_mask shape: (batch_size, 1, 1, input_seq_len)

        look_ahead_mask = create_look_ahead_mask(tf.shape(tar)[1])
        # look_ahead_mask shape: (target_seq_len, target_seq_len)
        dec_target_padding_mask = create_padding_mask(tar)
        # dec_target_padding_mask shape: (batch_size, 1, 1, target_seq_len)
        combined_mask = tf.maximum(dec_target_padding_mask, look_ahead_mask)
        dec_output, _ = self.decoder(tar, enc_output, training=training, 
                                     look_ahead_mask=combined_mask, 
                                     padding_mask=dec_padding_mask)
        # dec_output shape: (batch_size, target_seq_len, d_model)
        final_output = self.final_layer(dec_output)
        # final_output shape: (batch_size, target_seq_len, target_vocab_size)
        return final_output

# 最后是演示函数
def demo_transformer():
    # Transformer模型的层数
    num_layers = 4
    # 模型的维度，表示词嵌入的大小和模型内部表示的维度
    d_model = 128
    # 多头注意力机制中的头数
    num_heads = 8
    # 前馈神经网络的隐藏层大小
    dff = 512
    # 输入词汇表大小
    input_vocab_size = 8000
    # 输出词汇表大小
    target_vocab_size = 8000
    # 输入序列的最大位置编码长度
    pe_input = 10000
    # 输出序列的最大位置编码长度
    pe_target = 6000

    transformer = TransformerModel(num_layers, d_model, num_heads, dff,
                                   input_vocab_size, target_vocab_size,
                                   pe_input, pe_target)

    temp_input = tf.random.uniform((64, 62), dtype=tf.int32, maxval=input_vocab_size)
    # temp_input shape: (batch_size, input_seq_len) 
    temp_target = tf.random.uniform((64, 26), dtype=tf.int32, maxval=target_vocab_size)
    # temp_target shape: (batch_size, target_seq_len)

    inputs = (temp_input, temp_target)

    fn_out = transformer(inputs, training=False)

    print(f"输出形状: {fn_out.shape}")

if __name__ == "__main__":
    demo_transformer()
