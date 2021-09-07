"""
# @Author: Larkin
# @Date: 2021/9/6 16:27
# @Function:
# @ModuleName:fromTFrecords
"""
import os
import tensorflow as tf


def decode_and_normalize(serialized_example):
    """
    Decode and normalize an image and label from the given `serialized_example`.
    It is used as a map function for `dataset.map`
    """
    # 1. define a parser
    feature_dataset = tf.io.parse_single_example(
        serialized_example,
        # Defaults are not specified since both keys are required.
        features={
            'user_id': tf.io.FixedLenFeature([], tf.string),
            'target': tf.io.FixedLenFeature([1], tf.int64),
            'label': tf.io.FixedLenFeature([1], tf.int64),
            'neg_target': tf.io.FixedLenFeature([], tf.int64),
            'neg_label': tf.io.FixedLenFeature([], tf.int64),
            'padding': tf.io.FixedLenFeature([50], tf.int64),
        })
    # 2. decode the data
    user_id = feature_dataset['user_id']
    padding = tf.cast(feature_dataset['padding'], tf.int32)
    target = tf.cast(feature_dataset['target'], tf.int32)
    label = tf.cast(feature_dataset['label'], tf.int32)
    neg_target = feature_dataset['neg_target']
    neg_label = feature_dataset['neg_label']
    return (padding, target), label


# parsed_dataset = dataset.map(decode_and_normalize)
# filenames = [("C:\\tmp\\tfrecord-dnn\\train" + "/" + name) for name in os.listdir("C:\\tmp\\tfrecord-dnn\\train") if name.startswith("part")]
# dataset = tf.data.TFRecordDataset(filenames)
def get_trainORval_data(filenames_dir, batch_size):
    filenames = tf.io.gfile.glob(filenames_dir)
    print(filenames)
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.shuffle(512)
    parsed_dataset = dataset.map(decode_and_normalize)
    parsed_dataset = parsed_dataset.batch(batch_size)
    return parsed_dataset.repeat(3)


def get_test_data(filenames_dir, batch_size):
    filenames = tf.io.gfile.glob(filenames_dir)
    print(filenames)
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.shuffle(512)
    parsed_dataset = dataset.map(decode_and_normalize2)
    parsed_dataset = parsed_dataset.batch(batch_size)
    return parsed_dataset


# batch_size = 20

# parsed_dataset = parsed_dataset.batch(batch_size)
# for i in parsed_dataset:
#    print(i)
# print(parsed_dataset)
def decode_and_normalize2(serialized_example):
    """
    Decode and normalize an image and label from the given `serialized_example`.
    It is used as a map function for `dataset.map`
    """
    # 1. define a parser
    feature_dataset = tf.io.parse_single_example(
        serialized_example,
        # Defaults are not specified since both keys are required.
        features={
            'user_id': tf.io.FixedLenFeature([], tf.string),
            'target': tf.io.FixedLenFeature([1], tf.int64),
            'label': tf.io.FixedLenFeature([1], tf.int64),
            'padding': tf.io.FixedLenFeature([50], tf.int64),
        })
    # 2. decode the data
    user_id = feature_dataset['user_id']
    target = tf.cast(feature_dataset['target'], tf.int32)
    label = tf.cast(feature_dataset['label'], tf.int32)
    padding = tf.cast(feature_dataset['padding'], tf.int32)
    #
    return (padding, target), (user_id, label)


def sparseFeature(feat, feat_num, embed_dim=64):
    """
    create dictionary for sparse feature
    :param feat: feature name
    :param feat_num: the total number of sparse features that do not repeat
    :param embed_dim: embedding dimension
    :return:
    """
    return {'feat': feat, 'feat_num': feat_num, 'embed_dim': embed_dim}
